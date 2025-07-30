// WebSocket functionality for real-time communication

class WebSocketManager {
    constructor() {
        this.socket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectInterval = 5000; // 5 seconds
        this.isConnected = false;
        this.eventHandlers = new Map();
        this.analysisRooms = new Set();
    }
    
    // Initialize WebSocket connection
    initialize() {
        if (typeof io === 'undefined') {
            console.warn('Socket.IO not available, WebSocket features disabled');
            return false;
        }
        
        try {
            this.socket = io({
                transports: ['websocket', 'polling'],
                timeout: 10000,
                reconnection: true,
                reconnectionAttempts: this.maxReconnectAttempts,
                reconnectionDelay: 1000,
                reconnectionDelayMax: 5000
            });
            
            this.setupEventHandlers();
            console.log('WebSocket manager initialized');
            return true;
        } catch (error) {
            console.error('Failed to initialize WebSocket:', error);
            return false;
        }
    }
    
    // Setup core event handlers
    setupEventHandlers() {
        if (!this.socket) return;
        
        // Connection events
        this.socket.on('connect', () => {
            this.isConnected = true;
            this.reconnectAttempts = 0;
            console.log('WebSocket connected');
            
            this.showConnectionStatus('Connected to server', 'success');
            
            // Rejoin analysis rooms
            this.rejoinAnalysisRooms();
            
            // Trigger custom connect handlers
            this.triggerEvent('ws_connected');
        });
        
        this.socket.on('disconnect', (reason) => {
            this.isConnected = false;
            console.log('WebSocket disconnected:', reason);
            
            this.showConnectionStatus('Disconnected from server', 'warning');
            
            // Trigger custom disconnect handlers
            this.triggerEvent('ws_disconnected', { reason });
        });
        
        this.socket.on('connect_error', (error) => {
            console.error('WebSocket connection error:', error);
            this.showConnectionStatus('Connection error', 'error');
            
            // Trigger custom error handlers
            this.triggerEvent('ws_error', { error });
        });
        
        this.socket.on('reconnect', (attemptNumber) => {
            console.log('WebSocket reconnected after', attemptNumber, 'attempts');
            this.showConnectionStatus('Reconnected to server', 'success');
            
            // Trigger custom reconnect handlers
            this.triggerEvent('ws_reconnected', { attempts: attemptNumber });
        });
        
        this.socket.on('reconnect_error', (error) => {
            console.error('WebSocket reconnection error:', error);
            this.reconnectAttempts++;
            
            if (this.reconnectAttempts >= this.maxReconnectAttempts) {
                this.showConnectionStatus('Failed to reconnect', 'error');
            }
        });
        
        // Analysis-specific events
        this.socket.on('analysis_progress', (data) => {
            this.triggerEvent('analysis_progress', data);
        });
        
        this.socket.on('analysis_complete', (data) => {
            this.triggerEvent('analysis_complete', data);
        });
        
        this.socket.on('analysis_error', (data) => {
            this.triggerEvent('analysis_error', data);
        });
        
        // Server messages
        this.socket.on('server_message', (data) => {
            this.handleServerMessage(data);
        });
        
        // Heartbeat/ping for connection health
        this.socket.on('ping', () => {
            this.socket.emit('pong');
        });
    }
    
    // Join analysis room for updates
    joinAnalysis(analysisId) {
        if (!this.socket || !this.isConnected) {
            console.warn('Cannot join analysis room: WebSocket not connected');
            return false;
        }
        
        this.socket.emit('join_analysis', { analysis_id: analysisId });
        this.analysisRooms.add(analysisId);
        console.log('Joined analysis room:', analysisId);
        return true;
    }
    
    // Leave analysis room
    leaveAnalysis(analysisId) {
        if (!this.socket) return false;
        
        this.socket.emit('leave_analysis', { analysis_id: analysisId });
        this.analysisRooms.delete(analysisId);
        console.log('Left analysis room:', analysisId);
        return true;
    }
    
    // Rejoin all analysis rooms after reconnection
    rejoinAnalysisRooms() {
        this.analysisRooms.forEach(analysisId => {
            this.socket.emit('join_analysis', { analysis_id: analysisId });
        });
    }
    
    // Register event handler
    on(event, handler) {
        if (!this.eventHandlers.has(event)) {
            this.eventHandlers.set(event, []);
        }
        this.eventHandlers.get(event).push(handler);
    }
    
    // Remove event handler
    off(event, handler) {
        if (!this.eventHandlers.has(event)) return;
        
        const handlers = this.eventHandlers.get(event);
        const index = handlers.indexOf(handler);
        if (index > -1) {
            handlers.splice(index, 1);
        }
    }
    
    // Trigger custom event handlers
    triggerEvent(event, data = null) {
        if (!this.eventHandlers.has(event)) return;
        
        const handlers = this.eventHandlers.get(event);
        handlers.forEach(handler => {
            try {
                handler(data);
            } catch (error) {
                console.error('Error in event handler:', error);
            }
        });
    }
    
    // Send message to server
    emit(event, data = null) {
        if (!this.socket || !this.isConnected) {
            console.warn('Cannot emit event: WebSocket not connected');
            return false;
        }
        
        this.socket.emit(event, data);
        return true;
    }
    
    // Handle server messages
    handleServerMessage(data) {
        const { type, message, level = 'info' } = data;
        
        console.log('Server message:', message);
        
        // Show notification if available
        if (window.PsychAnalytica && window.PsychAnalytica.showNotification) {
            window.PsychAnalytica.showNotification(message, level);
        }
        
        // Trigger custom message handlers
        this.triggerEvent('server_message', data);
    }
    
    // Show connection status
    showConnectionStatus(message, type = 'info') {
        // Create or update connection status indicator
        let indicator = document.getElementById('connection-status');
        
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'connection-status';
            indicator.style.cssText = `
                position: fixed;
                top: 10px;
                right: 10px;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
                z-index: 10000;
                transition: all 0.3s ease;
                pointer-events: none;
            `;
            document.body.appendChild(indicator);
        }
        
        // Update indicator style based on type
        const styles = {
            success: {
                background: 'var(--text-success)',
                color: 'white'
            },
            warning: {
                background: 'var(--text-warning)',
                color: 'white'
            },
            error: {
                background: 'var(--text-error)',
                color: 'white'
            },
            info: {
                background: 'var(--text-accent)',
                color: 'white'
            }
        };
        
        const style = styles[type] || styles.info;
        indicator.style.background = style.background;
        indicator.style.color = style.color;
        indicator.textContent = message;
        
        // Auto-hide after 3 seconds for success messages
        if (type === 'success') {
            setTimeout(() => {
                if (indicator) {
                    indicator.style.opacity = '0';
                    setTimeout(() => {
                        if (indicator && indicator.parentNode) {
                            indicator.remove();
                        }
                    }, 300);
                }
            }, 3000);
        }
    }
    
    // Get connection status
    getConnectionStatus() {
        return {
            connected: this.isConnected,
            reconnectAttempts: this.reconnectAttempts,
            analysisRooms: Array.from(this.analysisRooms)
        };
    }
    
    // Disconnect WebSocket
    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            this.socket = null;
            this.isConnected = false;
            this.analysisRooms.clear();
            console.log('WebSocket disconnected manually');
        }
    }
    
    // Reconnect WebSocket
    reconnect() {
        if (this.socket) {
            this.socket.connect();
        } else {
            this.initialize();
        }
    }
}

// Create global WebSocket manager instance
const wsManager = new WebSocketManager();

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Small delay to ensure other scripts are loaded
    setTimeout(() => {
        wsManager.initialize();
    }, 1000);
});

// Analysis-specific WebSocket functions for backward compatibility
function initializeWebSocket(analysisId) {
    if (wsManager.initialize()) {
        // Wait for connection before joining
        if (wsManager.isConnected) {
            wsManager.joinAnalysis(analysisId);
        } else {
            wsManager.on('ws_connected', () => {
                wsManager.joinAnalysis(analysisId);
            });
        }
    }
}

// Page-specific event handlers
function setupAnalysisWebSocket(analysisId) {
    // Analysis progress updates
    wsManager.on('analysis_progress', (data) => {
        if (data.analysis_id === analysisId && window.AnalysisPage) {
            window.AnalysisPage.updateProgress(
                data.progress,
                data.current_step,
                data.step
            );
        }
    });
    
    // Analysis completion
    wsManager.on('analysis_complete', (data) => {
        if (data.analysis_id === analysisId) {
            // Show completion notification
            if (window.PsychAnalytica) {
                window.PsychAnalytica.showNotification(
                    'Analysis completed successfully!',
                    'success',
                    5000
                );
            }
            
            // Redirect to report page after short delay
            setTimeout(() => {
                window.location.href = `/report/${analysisId}`;
            }, 2000);
        }
    });
    
    // Analysis errors
    wsManager.on('analysis_error', (data) => {
        if (data.analysis_id === analysisId) {
            if (window.AnalysisPage) {
                window.AnalysisPage.showError(data.error);
            }
        }
    });
}

// Connection monitoring for UI feedback
function setupConnectionMonitoring() {
    wsManager.on('ws_connected', () => {
        // Update UI to show connected state
        const navBrand = document.querySelector('.nav-brand');
        if (navBrand) {
            const indicator = navBrand.querySelector('.connection-indicator');
            if (indicator) {
                indicator.style.color = 'var(--text-success)';
                indicator.title = 'Connected to server';
            }
        }
    });
    
    wsManager.on('ws_disconnected', () => {
        // Update UI to show disconnected state
        const navBrand = document.querySelector('.nav-brand');
        if (navBrand) {
            const indicator = navBrand.querySelector('.connection-indicator');
            if (indicator) {
                indicator.style.color = 'var(--text-warning)';
                indicator.title = 'Disconnected from server';
            }
        }
    });
}

// Add connection indicator to navigation
function addConnectionIndicator() {
    const navBrand = document.querySelector('.nav-brand');
    if (navBrand && !navBrand.querySelector('.connection-indicator')) {
        const indicator = document.createElement('div');
        indicator.className = 'connection-indicator';
        indicator.innerHTML = '<i class="fas fa-circle" style="font-size: 8px;"></i>';
        indicator.style.cssText = `
            color: var(--text-tertiary);
            margin-left: 8px;
            transition: color 0.3s ease;
        `;
        indicator.title = 'Connecting to server...';
        navBrand.appendChild(indicator);
    }
}

// Initialize connection monitoring
document.addEventListener('DOMContentLoaded', () => {
    addConnectionIndicator();
    setupConnectionMonitoring();
});

// Export WebSocket manager for global use
window.WebSocketManager = wsManager;
window.initializeWebSocket = initializeWebSocket;
window.setupAnalysisWebSocket = setupAnalysisWebSocket;

console.log('WebSocket.js loaded successfully');

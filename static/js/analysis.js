// Analysis page functionality for real-time progress tracking and updates

let analysisSocket = null;
let analysisId = null;
let startTime = null;
let progressInterval = null;
let currentStep = null;

// Analysis step configurations
const ANALYSIS_STEPS = {
    'market_research': {
        name: 'Market Research',
        description: 'Comprehensive multi-source market intelligence gathering',
        duration: 600, // 10 minutes
        progress: 10
    },
    'avatar_analysis': {
        name: 'Avatar Psychology Analysis',
        description: 'Deep psychological profiling of target audience',
        duration: 480, // 8 minutes
        progress: 25
    },
    'mental_drivers': {
        name: 'Mental Drivers Framework',
        description: 'Custom psychological triggers and anchoring mechanisms',
        duration: 420, // 7 minutes
        progress: 40
    },
    'objection_analysis': {
        name: 'Objection Analysis',
        description: 'Anti-objection engineering and counter-strategy development',
        duration: 360, // 6 minutes
        progress: 55
    },
    'provi_system': {
        name: 'Visual Proof System (PROVIs)',
        description: 'Physical demonstration system for abstract concepts',
        duration: 480, // 8 minutes
        progress: 70
    },
    'prepitch_architecture': {
        name: 'Pre-Pitch Architecture',
        description: 'Invisible persuasion sequence and psychological preparation',
        duration: 360, // 6 minutes
        progress: 85
    },
    'report_generation': {
        name: 'Report Generation',
        description: 'Comprehensive analysis compilation and formatting',
        duration: 300, // 5 minutes
        progress: 95
    },
    'pdf_generation': {
        name: 'PDF Generation',
        description: 'Professional document creation and formatting',
        duration: 120, // 2 minutes
        progress: 100
    }
};

// Initialize analysis tracking
function initializeAnalysisTracking(id) {
    analysisId = id;
    console.log('Initializing analysis tracking for:', analysisId);
    
    // Setup progress monitoring
    setupProgressMonitoring();
    
    // Setup step tracking
    setupStepTracking();
    
    // Setup error handling
    setupErrorHandling();
    
    // Start polling for updates
    startProgressPolling();
}

// Setup progress monitoring
function setupProgressMonitoring() {
    const progressFill = document.getElementById('progress-fill');
    const progressPercentage = document.getElementById('progress-percentage');
    
    if (!progressFill || !progressPercentage) {
        console.error('Progress elements not found');
        return;
    }
    
    // Initialize progress
    updateProgress(0, 'Initializing analysis...');
}

// Update progress display
function updateProgress(percentage, message, step = null) {
    const progressFill = document.getElementById('progress-fill');
    const progressPercentage = document.getElementById('progress-percentage');
    const currentStepTitle = document.getElementById('current-step-title');
    const currentStepDescription = document.getElementById('current-step-description');
    
    if (progressFill) {
        progressFill.style.width = percentage + '%';
    }
    
    if (progressPercentage) {
        progressPercentage.textContent = Math.round(percentage) + '%';
    }
    
    if (currentStepTitle && message) {
        currentStepTitle.textContent = message;
    }
    
    if (currentStepDescription && step && ANALYSIS_STEPS[step]) {
        currentStepDescription.textContent = ANALYSIS_STEPS[step].description;
    }
    
    // Update step indicators
    updateStepIndicators(step, percentage);
    
    // Add feed item
    addFeedItem(message);
    
    console.log(`Progress: ${percentage}% - ${message}`);
}

// Update step indicators in timeline
function updateStepIndicators(currentStepKey, progress) {
    const stepItems = document.querySelectorAll('.step-item');
    
    stepItems.forEach(item => {
        const stepKey = item.dataset.step;
        const stepConfig = ANALYSIS_STEPS[stepKey];
        
        if (!stepConfig) return;
        
        const statusIcons = item.querySelectorAll('.step-status i');
        const pendingIcon = item.querySelector('.step-pending');
        const activeIcon = item.querySelector('.step-active');
        const completeIcon = item.querySelector('.step-complete');
        
        // Reset all icons
        statusIcons.forEach(icon => icon.classList.add('hidden'));
        item.classList.remove('active', 'completed');
        
        if (progress >= stepConfig.progress) {
            // Step completed
            completeIcon?.classList.remove('hidden');
            item.classList.add('completed');
        } else if (stepKey === currentStepKey) {
            // Step active
            activeIcon?.classList.remove('hidden');
            item.classList.add('active');
        } else {
            // Step pending
            pendingIcon?.classList.remove('hidden');
        }
    });
}

// Add item to live feed
function addFeedItem(message) {
    const feed = document.getElementById('analysis-feed');
    if (!feed) return;
    
    const timestamp = new Date().toLocaleTimeString();
    const feedItem = document.createElement('div');
    feedItem.className = 'feed-item';
    feedItem.innerHTML = `
        <div class="feed-timestamp">${timestamp}</div>
        <div class="feed-message">${message}</div>
    `;
    
    feed.appendChild(feedItem);
    
    // Auto-scroll to bottom
    feed.scrollTop = feed.scrollHeight;
    
    // Keep only last 50 items
    const items = feed.querySelectorAll('.feed-item');
    if (items.length > 50) {
        items[0].remove();
    }
}

// Setup step tracking
function setupStepTracking() {
    const stepItems = document.querySelectorAll('.step-item');
    
    stepItems.forEach(item => {
        const stepKey = item.dataset.step;
        const stepConfig = ANALYSIS_STEPS[stepKey];
        
        if (stepConfig) {
            // Add click handler for step details
            item.addEventListener('click', () => {
                showStepDetails(stepKey, stepConfig);
            });
        }
    });
}

// Show step details modal
function showStepDetails(stepKey, stepConfig) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>${stepConfig.name}</h3>
                <button class="modal-close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <p>${stepConfig.description}</p>
                <div class="step-progress">
                    <strong>Estimated Duration:</strong> ${Math.round(stepConfig.duration / 60)} minutes<br>
                    <strong>Progress Target:</strong> ${stepConfig.progress}%
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close modal handlers
    const closeBtn = modal.querySelector('.modal-close');
    closeBtn.addEventListener('click', () => modal.remove());
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.remove();
    });
    
    // Remove modal on escape
    document.addEventListener('keydown', function escapeHandler(e) {
        if (e.key === 'Escape') {
            modal.remove();
            document.removeEventListener('keydown', escapeHandler);
        }
    });
}

// Start time tracking
function startTimeTracking(startTimeISO) {
    startTime = new Date(startTimeISO);
    
    const elapsedTimeEl = document.getElementById('elapsed-time');
    const remainingTimeEl = document.getElementById('remaining-time');
    const completionTimeEl = document.getElementById('completion-time');
    
    // Update time displays every second
    progressInterval = setInterval(() => {
        const now = new Date();
        const elapsed = Math.floor((now - startTime) / 1000);
        
        if (elapsedTimeEl) {
            elapsedTimeEl.textContent = formatTime(elapsed);
        }
        
        // Calculate estimated remaining time based on progress
        const progressFill = document.getElementById('progress-fill');
        if (progressFill && remainingTimeEl) {
            const currentProgress = parseFloat(progressFill.style.width) || 0;
            if (currentProgress > 0 && currentProgress < 100) {
                const totalEstimated = (elapsed / currentProgress) * 100;
                const remaining = Math.max(0, Math.floor(totalEstimated - elapsed));
                remainingTimeEl.textContent = formatTime(remaining);
                
                // Update estimated completion time
                if (completionTimeEl) {
                    const completionTime = new Date(now.getTime() + (remaining * 1000));
                    completionTimeEl.textContent = completionTime.toLocaleTimeString();
                }
            }
        }
    }, 1000);
}

// Setup error handling
function setupErrorHandling() {
    const errorSection = document.getElementById('error-section');
    const retryBtn = document.getElementById('retry-analysis');
    
    if (retryBtn) {
        retryBtn.addEventListener('click', () => {
            // Hide error section
            if (errorSection) {
                errorSection.classList.add('hidden');
            }
            
            // Restart analysis
            restartAnalysis();
        });
    }
}

// Show error state
function showError(message) {
    const errorSection = document.getElementById('error-section');
    const errorMessage = document.getElementById('error-message');
    
    if (errorSection) {
        errorSection.classList.remove('hidden');
    }
    
    if (errorMessage) {
        errorMessage.textContent = message;
    }
    
    // Stop progress polling
    if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
    }
    
    // Add error to feed
    addFeedItem(`ERROR: ${message}`);
    
    // Show notification
    if (window.PsychAnalytica) {
        window.PsychAnalytica.showNotification(message, 'error');
    }
}

// Start progress polling
function startProgressPolling() {
    const pollInterval = 2000; // Poll every 2 seconds
    
    const poll = async () => {
        try {
            const response = await fetch(`/api/analysis_status/${analysisId}`);
            const data = await response.json();
            
            if (data.status === 'completed') {
                handleAnalysisComplete(data);
                return;
            }
            
            if (data.status === 'error') {
                showError(data.error_message || 'Analysis failed');
                return;
            }
            
            if (data.status === 'processing') {
                updateProgress(
                    data.progress || 0,
                    data.current_step || 'Processing...',
                    getCurrentStepKey(data.current_step)
                );
            }
            
            // Continue polling
            setTimeout(poll, pollInterval);
            
        } catch (error) {
            console.error('Polling error:', error);
            showError('Failed to get analysis status');
        }
    };
    
    // Start polling
    poll();
}

// Get current step key from message
function getCurrentStepKey(message) {
    if (!message) return null;
    
    const lowerMessage = message.toLowerCase();
    
    for (const [key, config] of Object.entries(ANALYSIS_STEPS)) {
        if (lowerMessage.includes(key.replace('_', ' ')) || 
            lowerMessage.includes(config.name.toLowerCase())) {
            return key;
        }
    }
    
    return null;
}

// Handle analysis completion
function handleAnalysisComplete(data) {
    // Stop polling
    if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
    }
    
    // Update progress to 100%
    updateProgress(100, 'Analysis completed successfully!');
    
    // Show completion notification
    if (window.PsychAnalytica) {
        window.PsychAnalytica.showNotification(
            `Analysis completed! Report contains ${data.report_word_count?.toLocaleString() || 'thousands of'} words.`,
            'success',
            8000
        );
    }
    
    // Show view report button
    const viewReportBtn = document.getElementById('view-report');
    if (viewReportBtn) {
        viewReportBtn.style.display = 'inline-flex';
        viewReportBtn.addEventListener('click', () => {
            window.location.href = `/report/${analysisId}`;
        });
    }
    
    // Add completion to feed
    addFeedItem('Analysis completed successfully! Report is ready for viewing.');
    
    // Animate completion
    animateCompletion();
}

// Animate completion state
function animateCompletion() {
    const progressCard = document.querySelector('.progress-card');
    if (progressCard) {
        progressCard.style.background = 'linear-gradient(145deg, #1a4d3a 0%, #0f2f24 100%)';
        progressCard.style.border = '2px solid var(--text-success)';
        
        // Add success icon to current step
        const stepIcon = document.querySelector('.step-icon');
        if (stepIcon) {
            stepIcon.innerHTML = '<i class="fas fa-check" style="color: var(--text-success); font-size: 1.5rem;"></i>';
        }
    }
    
    // Animate all step items to completed
    const stepItems = document.querySelectorAll('.step-item');
    stepItems.forEach((item, index) => {
        setTimeout(() => {
            const statusIcons = item.querySelectorAll('.step-status i');
            const completeIcon = item.querySelector('.step-complete');
            
            statusIcons.forEach(icon => icon.classList.add('hidden'));
            completeIcon?.classList.remove('hidden');
            item.classList.add('completed');
        }, index * 200);
    });
}

// Restart analysis
function restartAnalysis() {
    // Reset UI state
    const progressFill = document.getElementById('progress-fill');
    const progressPercentage = document.getElementById('progress-percentage');
    
    if (progressFill) progressFill.style.width = '0%';
    if (progressPercentage) progressPercentage.textContent = '0%';
    
    // Reset step indicators
    const stepItems = document.querySelectorAll('.step-item');
    stepItems.forEach(item => {
        const statusIcons = item.querySelectorAll('.step-status i');
        const pendingIcon = item.querySelector('.step-pending');
        
        statusIcons.forEach(icon => icon.classList.add('hidden'));
        pendingIcon?.classList.remove('hidden');
        item.classList.remove('active', 'completed');
    });
    
    // Clear feed
    const feed = document.getElementById('analysis-feed');
    if (feed) {
        feed.innerHTML = `
            <div class="feed-item">
                <div class="feed-timestamp">${new Date().toLocaleTimeString()}</div>
                <div class="feed-message">Analysis restarted</div>
            </div>
        `;
    }
    
    // Restart time tracking
    startTime = new Date();
    
    // Restart polling
    startProgressPolling();
    
    // Show notification
    if (window.PsychAnalytica) {
        window.PsychAnalytica.showNotification('Analysis restarted', 'info');
    }
}

// Initialize WebSocket connection
function initializeWebSocket(id) {
    analysisId = id;
    
    // Only initialize WebSocket if Socket.IO is available
    if (typeof io !== 'undefined') {
        analysisSocket = io();
        
        analysisSocket.on('connect', () => {
            console.log('Connected to analysis WebSocket');
            analysisSocket.emit('join_analysis', { analysis_id: analysisId });
        });
        
        analysisSocket.on('disconnect', () => {
            console.log('Disconnected from analysis WebSocket');
        });
        
        analysisSocket.on('analysis_progress', (data) => {
            if (data.analysis_id === analysisId) {
                updateProgress(
                    data.progress,
                    data.current_step,
                    data.step
                );
            }
        });
        
        analysisSocket.on('analysis_complete', (data) => {
            if (data.analysis_id === analysisId) {
                handleAnalysisComplete(data);
            }
        });
        
        analysisSocket.on('analysis_error', (data) => {
            if (data.analysis_id === analysisId) {
                showError(data.error);
            }
        });
    }
}

// Toggle live feed visibility
function setupFeedToggle() {
    const toggleBtn = document.getElementById('toggle-feed');
    const feed = document.getElementById('analysis-feed');
    
    if (toggleBtn && feed) {
        toggleBtn.addEventListener('click', () => {
            const isHidden = feed.style.display === 'none';
            
            if (isHidden) {
                feed.style.display = 'block';
                toggleBtn.innerHTML = '<i class="fas fa-eye-slash"></i><span>Hide Details</span>';
            } else {
                feed.style.display = 'none';
                toggleBtn.innerHTML = '<i class="fas fa-eye"></i><span>Show Details</span>';
            }
        });
    }
}

// Utility function to format time (MM:SS)
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

// Setup download functionality
function setupDownloadHandlers() {
    const downloadBtn = document.getElementById('download-pdf');
    
    if (downloadBtn) {
        downloadBtn.addEventListener('click', () => {
            window.location.href = `/api/download_report/${analysisId}`;
        });
    }
}

// Initialize page functionality
document.addEventListener('DOMContentLoaded', () => {
    setupFeedToggle();
    setupDownloadHandlers();
});

// Export functions for global use
window.AnalysisPage = {
    initializeAnalysisTracking,
    startTimeTracking,
    initializeWebSocket,
    updateProgress,
    showError,
    formatTime
};

console.log('Analysis.js loaded successfully');

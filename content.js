console.log("Random Episode Picker script loaded!");

let lastDetectedTime = null;
let checkInterval = null;

// Function to monitor the "time-remaining-label" every second
function monitorTimeRemaining() {
  const timeLabel = document.querySelector(".time-remaining-label");

  if (timeLabel) {
    console.log("Found 'time-remaining-label'. Monitoring for updates...");

    // Start checking the label's text every second
    checkInterval = setInterval(() => {
      if (timeLabel.innerText) {
        checkTimeRemaining(timeLabel.innerText);
      }
    }, 5000);
  } else {
    console.log("'time-remaining-label' not found. Retrying in 2 seconds...");
    setTimeout(monitorTimeRemaining, 2000); // Retry if not found
  }
}

// Function to extract time and trigger new episode when < 1 min remains
function checkTimeRemaining(text) {
  const match = text.match(/(?:(\d+):)?(\d{1,2}):(\d{2})/);
  // Matches "0:00", "00:00", "0:00:00", "00:00:00"

  if (match) {
    const hours = match[1] ? parseInt(match[1], 10) : 0;
    const minutes = parseInt(match[2], 10);
    const seconds = parseInt(match[3], 10);

    const totalSecondsLeft = hours * 3600 + minutes * 60 + seconds;
    console.log(`Time remaining: ${hours}h ${minutes}m ${seconds}s`);

    // If less than 60 seconds remains, request a new episode
    if (
      totalSecondsLeft > 0 &&
      totalSecondsLeft < 60 &&
      lastDetectedTime !== totalSecondsLeft
    ) {
      lastDetectedTime = totalSecondsLeft; // Prevent multiple triggers
      console.log("Episode ending soon! Requesting a new one...");
      clearInterval(checkInterval); // Stop checking to avoid multiple triggers
      chrome.runtime.sendMessage({ action: "pickRandomShow" });
    }
  }
}

// Start monitoring when the page loads
monitorTimeRemaining();

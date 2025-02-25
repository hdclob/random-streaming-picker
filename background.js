class EpisodeManager {
  constructor() {
    this.shows = {};
    this.services = {
      "Disney+": "https://www.disneyplus.com/play/",
    };

    this.maxConsecutive = 2;
    this.consecutiveCount = 0;
    this.currentShow = null;
  }

  fetchShowData() {
    return fetch(chrome.runtime.getURL("disney_episodes.json"))
      .then((response) => response.json())
      .then((data) => {
        this.shows["Disney+"] = Object.entries(data).map(
          ([showName, seasons]) => ({
            name: showName,
            episodes: Object.values(seasons).flat(), // Flatten all episodes across seasons
          })
        );
        console.log("Loaded shows:", this.shows);
      })
      .catch((error) => console.error("Error loading JSON:", error));
  }

  getNextShow() {
    if (
      this.currentShow == null ||
      this.consecutiveCount >= this.maxConsecutive
    ) {
      this.consecutiveCount = 0;
      let randomShow;
      do {
        randomShow =
          this.shows["Disney+"][
            Math.floor(Math.random() * this.shows["Disney+"].length)
          ];
      } while (this.currentShow == randomShow);

      this.currentShow = randomShow;
    }

    this.consecutiveCount++;
    return this.currentShow;
  }

  getNextEpisode(show) {
    return new Promise((resolve, reject) => {
      chrome.storage.local.get({ [show.name]: null }, function (result) {
        let lastEpisodeIdx = result[show.name];

        if (lastEpisodeIdx === null) {
          lastEpisodeIdx = -1;
        }
        lastEpisodeIdx++;

        if (typeof show.episodes[lastEpisodeIdx] === "undefined") {
          lastEpisodeIdx = 0;
        }

        chrome.storage.local.set({ [show.name]: lastEpisodeIdx });
        resolve(show.episodes[lastEpisodeIdx]);
      });
    });
  }

  async playEpisode(sender, consecutiveEpisodes = null) {
    if (consecutiveEpisodes != null) {
      this.maxConsecutive = consecutiveEpisodes;
    }
    this.currentShow = this.getNextShow();

    const nextEpisode = await this.getNextEpisode(this.currentShow);

    const url = this.services["Disney+"] + nextEpisode;

    if (sender?.tab?.id) {
      chrome.tabs.update(sender.tab.id, { url });
    } else {
      chrome.tabs.create({ url });
    }
  }
}

const episodeManager = new EpisodeManager();

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "pickRandomShow") {
    if (Object.keys(episodeManager.shows).length < 1) {
      episodeManager.fetchShowData().then(() => {
        episodeManager.playEpisode(sender, message.consecutiveEpisodes);
      });
    } else {
      episodeManager.playEpisode(sender, message.consecutiveEpisodes);
    }
  }
});

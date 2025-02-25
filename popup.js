document.getElementById("randomPick").addEventListener("click", () => {
  const consecutiveEpisodesInput = document.getElementById(
    "consecutiveEpisodes"
  );

  let consecutiveEpisodes = consecutiveEpisodesInput.value;
  try {
    consecutiveEpisodes = parseInt(consecutiveEpisodes);
  } catch (error) {
    consecutiveEpisodes = 2;
  }

  chrome.runtime.sendMessage({
    action: "pickRandomShow",
    consecutiveEpisodes: consecutiveEpisodes,
  });
});

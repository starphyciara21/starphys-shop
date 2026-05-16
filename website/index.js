/**
 * Sends a request to the server to delete a specific note.
 * @param {number} noteId - The ID of the note to be deleted.
 */
function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
    headers: {
      "Content-Type": "application/json",
    },
  }).then((_res) => {
    // Reload the page once the server confirms deletion
    window.location.href = "/";
  });
}
/* Outputs-page navigation. Keep the destination out of the HTML markup. */
document.addEventListener("click", (event) => {
  const control = event.target.closest('[data-action="homepage"]');
  if (!control) return;
  window.location.assign("index.html");
});

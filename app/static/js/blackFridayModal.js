document.addEventListener("DOMContentLoaded", function () {
  const openBtn = document.getElementById("btnApuntarme");
  const overlay = document.getElementById("bfModalOverlay");
  const closeBtn = document.getElementById("bfClose");
  const cancelBtn = document.getElementById("bfCancel");
  const emailInput = document.getElementById("bfEmail");

  function openModal() {
    overlay.classList.add("is-open");
    overlay.setAttribute("aria-hidden", "false");
    setTimeout(() => emailInput && emailInput.focus(), 0);
  }

  function closeModal() {
    overlay.classList.remove("is-open");
    overlay.setAttribute("aria-hidden", "true");
  }

  openBtn.addEventListener("click", openModal);
  closeBtn.addEventListener("click", closeModal);
  cancelBtn.addEventListener("click", closeModal);

  overlay.addEventListener("click", function (e) {
    if (e.target === overlay) closeModal();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeModal();
  });
});

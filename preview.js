const preview = document.createElement("div");
preview.className = "image-preview";
preview.hidden = true;
preview.setAttribute("aria-hidden", "true");
const photo = document.createElement("img");
photo.alt = "";
preview.append(photo);
document.body.append(preview);

let activeLink = null;
let anchor = { x: 0, y: 0 };

function positionPreview() {
  const gap = 16;
  const bounds = preview.getBoundingClientRect();
  let x = anchor.x + gap;
  let y = anchor.y + gap;
  if (x + bounds.width > window.innerWidth - gap) {
    x = anchor.x - bounds.width - gap;
  }
  if (y + bounds.height > window.innerHeight - gap) {
    y = anchor.y - bounds.height - gap;
  }
  preview.style.left = `${Math.max(gap, x)}px`;
  preview.style.top = `${Math.max(gap, y)}px`;
}

function hidePreview() {
  activeLink = null;
  preview.hidden = true;
}

function showPreview(link, x, y) {
  activeLink = link;
  anchor = { x, y };
  preview.hidden = true;
  photo.src = link.href;
  if (photo.complete && photo.naturalWidth) {
    preview.hidden = false;
    positionPreview();
  }
}

photo.addEventListener("load", () => {
  if (!activeLink) return;
  preview.hidden = false;
  positionPreview();
});
photo.addEventListener("error", () => { preview.hidden = true; });

document.querySelectorAll(".journal-project a, a[data-preview]").forEach((link) => {
  link.addEventListener("pointerenter", (event) => {
    if (event.pointerType === "touch") return;
    showPreview(link, event.clientX, event.clientY);
  });
  link.addEventListener("pointermove", (event) => {
    if (activeLink !== link) return;
    anchor = { x: event.clientX, y: event.clientY };
    positionPreview();
  });
  link.addEventListener("pointerleave", hidePreview);
  link.addEventListener("focus", () => {
    const bounds = link.getBoundingClientRect();
    showPreview(link, bounds.left, bounds.bottom);
  });
  link.addEventListener("blur", hidePreview);
  link.addEventListener("click", hidePreview);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") hidePreview();
});
window.addEventListener("scroll", hidePreview, { passive: true });
window.addEventListener("resize", hidePreview);


import { useEffect } from "react";

export default function Modal({
  isOpen,
  onClose,
  title,
  children,
  footer,
  size = "md",
  closeOnBackdrop = true,
  showCloseButton = true,
}) {
  const sizes = {
    sm: "max-w-md",
    md: "max-w-xl",
    lg: "max-w-3xl",
    xl: "max-w-5xl",
    full: "max-w-[calc(100vw-2rem)]",
  };

  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (event) => {
      if (event.key === "Escape") {
        onClose?.();
      }
    };

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      role="presentation"
    >
      <button
        type="button"
        aria-label="Close modal"
        className="absolute inset-0 h-full w-full cursor-default bg-black/70"
        onClick={closeOnBackdrop ? onClose : undefined}
        tabIndex={closeOnBackdrop ? 0 : -1}
        disabled={!closeOnBackdrop}
      />

      <section
        role="dialog"
        aria-modal="true"
        aria-labelledby={title ? "darkops-modal-title" : undefined}
        className={`relative z-10 flex max-h-[90vh] w-full flex-col overflow-hidden rounded-2xl border border-zinc-800 bg-[var(--color-agency-card)] shadow-2xl ${sizes[size] || sizes.md}`}
      >
        {(title || showCloseButton) && (
          <header className="flex shrink-0 items-center justify-between gap-4 border-b border-zinc-800 px-6 py-4">
            {title && (
              <h2
                id="darkops-modal-title"
                className="text-lg font-semibold text-white"
              >
                {title}
              </h2>
            )}

            {showCloseButton && (
              <button
                type="button"
                onClick={onClose}
                aria-label="Close modal"
                className="ml-auto flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-zinc-700 text-gray-400 focus-visible:outline-2 focus-visible:outline-[var(--color-agency-orange)]"
              >
                <svg
                  viewBox="0 0 24 24"
                  className="h-5 w-5"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  aria-hidden="true"
                >
                  <path d="m18 6-12 12M6 6l12 12" />
                </svg>
              </button>
            )}
          </header>
        )}

        <div className="min-h-0 flex-1 overflow-y-auto px-6 py-5 text-sm text-gray-300">
          {children}
        </div>

        {footer && (
          <footer className="flex shrink-0 flex-wrap items-center justify-end gap-3 border-t border-zinc-800 px-6 py-4">
            {footer}
          </footer>
        )}
      </section>
    </div>
  );
}

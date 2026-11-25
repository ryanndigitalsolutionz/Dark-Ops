
export default function HamburgerIcon({
  isOpen = false,
  onClick,
  className = "",
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={isOpen ? "Close navigation" : "Open navigation"}
      aria-expanded={isOpen}
      className={`flex h-10 w-10 items-center justify-center rounded-lg border border-zinc-800 bg-[var(--color-agency-card)] text-gray-300 focus-visible:outline-2 focus-visible:outline-[var(--color-agency-orange)] ${className}`}
    >
      <svg
        viewBox="0 0 24 24"
        className="h-5 w-5"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
      >
        {isOpen ? (
          <path d="m18 6-12 12M6 6l12 12" />
        ) : (
          <path d="M4 6h16M4 12h16M4 18h16" />
        )}
      </svg>
    </button>
  );
}


export default function TopBar({
  message,
  type = "info",
  action,
  onAction,
  visible = true,
}) {
  if (!visible || !message) return null;

  const variants = {
    info: "border-zinc-700 bg-[#1c1f26] text-gray-300",
    success: "border-green-900 bg-green-950/30 text-green-300",
    warning: "border-yellow-900 bg-yellow-950/30 text-yellow-300",
    critical: "border-red-900 bg-red-950/30 text-red-300",
  };

  return (
    <div
      role="status"
      className={`flex min-h-[46px] w-full items-center justify-between gap-4 border-b px-4 py-2 ${variants[type] || variants.info}`}
    >
      <p className="min-w-0 text-xs leading-relaxed">
        {message}
      </p>

      {action && (
        <button
          type="button"
          onClick={onAction}
          className="shrink-0 text-xs font-semibold underline underline-offset-4 focus-visible:outline-2 focus-visible:outline-[var(--color-agency-orange)]"
        >
          {action}
        </button>
      )}
    </div>
  );
}

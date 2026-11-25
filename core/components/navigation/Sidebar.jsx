
export default function Sidebar({
  items = [],
  activeItem,
  onNavigate,
  isOpen = false,
  onClose,
  logo,
  footer,
}) {
  return (
    <>
      {isOpen && (
        <button
          type="button"
          aria-label="Close sidebar"
          onClick={onClose}
          className="fixed inset-0 z-40 bg-black/60 lg:hidden"
        />
      )}

      <aside
        className={`fixed inset-y-0 left-0 z-50 flex w-64 flex-col border-r border-zinc-800 bg-[var(--color-agency-bg)] transition-transform duration-300 lg:static lg:translate-x-0 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex h-[72px] shrink-0 items-center border-b border-zinc-800 px-5">
          {logo || (
            <span className="text-lg font-semibold tracking-wider text-white">
              DARK<span className="text-[var(--color-agency-orange)]">OPS</span>
            </span>
          )}
        </div>

        <nav className="flex-1 space-y-1 overflow-y-auto p-3">
          {items.map((item) => {
            const isActive = activeItem === item.id;

            return (
              <button
                key={item.id}
                type="button"
                onClick={() => {
                  onNavigate?.(item);
                  onClose?.();
                }}
                aria-current={isActive ? "page" : undefined}
                className={`flex w-full items-center gap-3 rounded-lg px-3 py-3 text-left text-sm ${
                  isActive
                    ? "border border-orange-900/50 bg-orange-950/30 text-[var(--color-agency-orange)]"
                    : "border border-transparent text-gray-400"
                }`}
              >
                {item.icon && (
                  <span className="flex h-5 w-5 shrink-0 items-center justify-center">
                    {item.icon}
                  </span>
                )}

                <span className="truncate">{item.label}</span>
              </button>
            );
          })}
        </nav>

        {footer && (
          <div className="shrink-0 border-t border-zinc-800 p-4">
            {footer}
          </div>
        )}
      </aside>
    </>
  );
}

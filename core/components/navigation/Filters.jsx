
export default function Filters({
  search = "",
  onSearchChange,
  status = "all",
  onStatusChange,
  statuses = [],
  placeholder = "Search records...",
  children,
}) {
  return (
    <div className="flex flex-wrap items-center gap-3">
      <div className="relative min-w-[200px] flex-1">
        <svg
          viewBox="0 0 24 24"
          className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
        >
          <circle cx="11" cy="11" r="8" />
          <path d="m21 21-4.35-4.35" />
        </svg>

        <input
          type="search"
          value={search}
          onChange={(event) => onSearchChange?.(event.target.value)}
          placeholder={placeholder}
          className="w-full rounded-xl border border-zinc-800 bg-[var(--color-agency-card)] py-2.5 pl-10 pr-4 text-sm text-white outline-none focus:border-[var(--color-agency-orange)]"
        />
      </div>

      {statuses.length > 0 && (
        <select
          value={status}
          onChange={(event) => onStatusChange?.(event.target.value)}
          className="rounded-xl border border-zinc-800 bg-[var(--color-agency-card)] px-4 py-2.5 text-sm text-gray-300 outline-none focus:border-[var(--color-agency-orange)]"
        >
          <option value="all">All statuses</option>

          {statuses.map((item) => (
            <option key={item.value} value={item.value}>
              {item.label}
            </option>
          ))}
        </select>
      )}

      {children}
    </div>
  );
}

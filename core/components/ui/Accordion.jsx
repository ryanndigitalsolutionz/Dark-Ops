
import { useState, useId } from "react";

export default function Accordion({
  items = [],
  allowMultiple = false,
  defaultOpen = [],
  className = "",
}) {
  const baseId = useId();

  const [openItems, setOpenItems] = useState(
    Array.isArray(defaultOpen) ? defaultOpen : [defaultOpen]
  );

  const toggleItem = (itemId) => {
    setOpenItems((current) => {
      const isOpen = current.includes(itemId);

      if (isOpen) {
        return current.filter((id) => id !== itemId);
      }

      return allowMultiple ? [...current, itemId] : [itemId];
    });
  };

  return (
    <div
      className={`w-full overflow-hidden rounded-xl border border-zinc-800 bg-[var(--color-agency-card)] ${className}`}
    >
      {items.map((item, index) => {
        const itemId = item.id ?? index;
        const isOpen = openItems.includes(itemId);
        const triggerId = `${baseId}-trigger-${index}`;
        const panelId = `${baseId}-panel-${index}`;

        return (
          <section
            key={itemId}
            className={index !== 0 ? "border-t border-zinc-800" : ""}
          >
            <button
              id={triggerId}
              type="button"
              className={`flex w-full items-center justify-between gap-4 px-5 py-4 text-left transition-colors duration-200 focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-[var(--color-agency-orange)] disabled:cursor-not-allowed disabled:opacity-50 ${
                isOpen
                  ? "bg-zinc-800/70 text-white"
                  : "bg-transparent text-gray-300"
              }`}
              onClick={() => toggleItem(itemId)}
              aria-expanded={isOpen}
              aria-controls={panelId}
              disabled={item.disabled}
            >
              <span className="min-w-0 font-medium">
                {item.title}
              </span>

              <svg
                className={`h-4 w-4 shrink-0 ${
                  isOpen
                    ? "text-[var(--color-agency-orange)]"
                    : "text-gray-500"
                }`}
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                {isOpen ? (
                  <path d="m18 15-6-6-6 6" />
                ) : (
                  <path d="m6 9 6 6 6-6" />
                )}
              </svg>
            </button>

            {isOpen && (
              <div
                id={panelId}
                role="region"
                aria-labelledby={triggerId}
                className="border-t border-zinc-800 px-5 py-4 text-sm leading-relaxed text-gray-400"
              >
                {item.content}
              </div>
            )}
          </section>
        );
      })}
    </div>
  );
}

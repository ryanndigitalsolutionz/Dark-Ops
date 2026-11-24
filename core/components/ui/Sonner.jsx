
import { useEffect } from "react";

const variants = {
  success: {
    color: "border-l-green-500",
    icon: "✓",
    iconColor: "text-green-500",
  },
  error: {
    color: "border-l-red-500",
    icon: "×",
    iconColor: "text-red-500",
  },
  warning: {
    color: "border-l-yellow-500",
    icon: "!",
    iconColor: "text-yellow-500",
  },
  info: {
    color: "border-l-blue-500",
    icon: "i",
    iconColor: "text-blue-500",
  },
};

function ToastItem({ toast, onDismiss }) {
  const variant = variants[toast.type] || variants.info;

  useEffect(() => {
    if (toast.duration === 0) return;

    const timer = window.setTimeout(() => {
      onDismiss(toast.id);
    }, toast.duration ?? 4000);

    return () => window.clearTimeout(timer);
  }, [toast, onDismiss]);

  return (
    <div
      role={toast.type === "error" ? "alert" : "status"}
      className={`flex w-full max-w-sm items-start gap-3 rounded-xl border border-zinc-800 border-l-4 ${variant.color} bg-[#16181d] p-4 shadow-xl`}
    >
      <span
        className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-zinc-800 text-sm font-bold ${variant.iconColor}`}
        aria-hidden="true"
      >
        {variant.icon}
      </span>

      <div className="min-w-0 flex-1">
        {toast.title && (
          <p className="text-sm font-semibold text-white">
            {toast.title}
          </p>
        )}

        {toast.description && (
          <p className="mt-1 text-xs leading-relaxed text-gray-400">
            {toast.description}
          </p>
        )}
      </div>

      <button
        type="button"
        onClick={() => onDismiss(toast.id)}
        aria-label="Dismiss notification"
        className="shrink-0 text-gray-500 focus-visible:outline-2 focus-visible:outline-[var(--color-agency-orange)]"
      >
        ×
      </button>
    </div>
  );
}

export default function Sonner({
  toasts = [],
  onDismiss = () => {},
  position = "top-right",
}) {
  const positions = {
    "top-right": "right-4 top-4",
    "top-left": "left-4 top-4",
    "bottom-right": "right-4 bottom-4",
    "bottom-left": "left-4 bottom-4",
    "top-center": "left-1/2 top-4 -translate-x-1/2",
    "bottom-center": "bottom-4 left-1/2 -translate-x-1/2",
  };

  return (
    <div
      aria-label="Notifications"
      className={`pointer-events-none fixed z-[100] flex w-[calc(100%-2rem)] max-w-sm flex-col gap-3 ${positions[position] || positions["top-right"]}`}
    >
      {toasts.map((toast) => (
        <div key={toast.id} className="pointer-events-auto">
          <ToastItem toast={toast} onDismiss={onDismiss} />
        </div>
      ))}
    </div>
  );
}

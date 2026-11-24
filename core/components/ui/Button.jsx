
const variants = {
  primary: [
    "bg-[var(--color-agency-orange)] text-white border border-[var(--color-agency-orange)]",
    "hover:bg-white hover:text-[var(--color-agency-orange)] hover:border-white",
  ].join(" "),

  secondary: [
    "bg-transparent text-gray-200 border border-zinc-600",
    "hover:bg-white hover:text-zinc-900 hover:border-white",
  ].join(" "),

  danger: [
    "bg-red-600 text-white border border-red-600",
    "hover:bg-white hover:text-red-600 hover:border-white",
  ].join(" "),

  ghost: [
    "bg-transparent text-gray-300 border border-transparent",
    "hover:bg-[var(--color-agency-orange)] hover:text-white hover:border-[var(--color-agency-orange)]",
  ].join(" "),
};

const sizes = {
  sm: "px-3 py-1.5 text-xs rounded-lg",
  md: "px-4 py-2.5 text-sm rounded-xl",
  lg: "px-6 py-3 text-base rounded-xl",
};

export default function Button({
  children,
  variant = "primary",
  size = "md",
  type = "button",
  disabled = false,
  loading = false,
  onClick,
  className = "",
  ...props
}) {
  const buttonClasses = [
    "inline-flex items-center justify-center gap-2",
    "font-medium font-[var(--font-montserrat)]",
    "transition-colors duration-200 ease-in-out",
    "focus-visible:outline-none focus-visible:ring-2",
    "focus-visible:ring-[var(--color-agency-orange)]",
    "focus-visible:ring-offset-2 focus-visible:ring-offset-[var(--color-agency-bg)]",
    "disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none",
    variants[variant] || variants.primary,
    sizes[size] || sizes.md,
    className,
  ].join(" ");

  return (
    <button
      type={type}
      className={buttonClasses}
      disabled={disabled || loading}
      onClick={onClick}
      aria-busy={loading}
      {...props}
    >
      {loading && (
        <span
          className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent"
          aria-hidden="true"
        />
      )}

      {children}
    </button>
  );
}

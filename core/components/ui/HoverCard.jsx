
import { useEffect, useState } from "react";

export default function HoverCard({
  children,
  content,
  placement = "top",
  delay = 2000,
  className = "",
}) {
  const [isVisible, setIsVisible] = useState(false);
  const [isActive, setIsActive] = useState(false);

  useEffect(() => {
    if (!isActive) {
      setIsVisible(false);
      return;
    }

    const timer = window.setTimeout(() => {
      setIsVisible(true);
    }, delay);

    return () => window.clearTimeout(timer);
  }, [isActive, delay]);

  const placements = {
    top: "bottom-full left-1/2 -translate-x-1/2",
    bottom: "top-full left-1/2 -translate-x-1/2",
    left: "right-full top-1/2 -translate-y-1/2",
    right: "left-full top-1/2 -translate-y-1/2",
  };

  const animationPositions = {
    top: {
      hidden: "top-2",
      visible: "top-0",
    },
    bottom: {
      hidden: "bottom-2",
      visible: "bottom-0",
    },
    left: {
      hidden: "right-2",
      visible: "right-0",
    },
    right: {
      hidden: "left-2",
      visible: "left-0",
    },
  };

  const position = animationPositions[placement] || animationPositions.top;

  return (
    <span
      className={`relative inline-flex ${className}`}
      onMouseEnter={() => setIsActive(true)}
      onMouseLeave={() => setIsActive(false)}
      onFocus={() => setIsActive(true)}
      onBlur={(event) => {
        if (!event.currentTarget.contains(event.relatedTarget)) {
          setIsActive(false);
        }
      }}
    >
      {children}

      <span
        role="tooltip"
        aria-hidden={!isVisible}
        className={`pointer-events-none absolute z-50 w-max max-w-xs transition-all duration-500 ease-out ${
          placements[placement] || placements.top
        } ${
          placement === "top" || placement === "bottom"
            ? isVisible
              ? position.visible
              : position.hidden
            : ""
        } ${
          placement === "left" || placement === "right"
            ? isVisible
              ? position.visible
              : position.hidden
            : ""
        } ${
          isVisible
            ? "visible opacity-100"
            : "invisible opacity-0"
        }`}
      >
        <span className="block rounded-lg border border-zinc-700 bg-zinc-900 px-3 py-2 text-xs leading-relaxed text-gray-200 shadow-xl">
          {content}
        </span>
      </span>
    </span>
  );
}

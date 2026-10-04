const menuToggle = document.querySelector(".menu-toggle");
const navigation = document.querySelector(".primary-nav");

if (menuToggle && navigation) {
    const closeMenu = () => {
        menuToggle.setAttribute("aria-expanded", "false");
        menuToggle.setAttribute("aria-label", "Open navigation");
        navigation.classList.remove("is-open");
    };

    menuToggle.addEventListener("click", () => {
        const isExpanded = menuToggle.getAttribute("aria-expanded") === "true";
        menuToggle.setAttribute("aria-expanded", String(!isExpanded));
        menuToggle.setAttribute("aria-label", isExpanded ? "Open navigation" : "Close navigation");
        navigation.classList.toggle("is-open", !isExpanded);
    });

    navigation.addEventListener("click", (event) => {
        if (event.target instanceof HTMLAnchorElement) {
            closeMenu();
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeMenu();
            menuToggle.focus();
        }
    });
}

const copyButton = document.querySelector(".copy-button");
const copyStatus = document.querySelector(".copy-status");

if (copyButton && copyStatus) {
    copyButton.addEventListener("click", async () => {
        const text = copyButton.getAttribute("data-copy");
        const label = copyButton.querySelector(".copy-label");

        if (!text || !label) {
            copyStatus.textContent = "Could not find the deploy command.";
            return;
        }

        try {
            if (navigator.clipboard && window.isSecureContext) {
                await navigator.clipboard.writeText(text);
            } else {
                const temporaryInput = document.createElement("textarea");
                temporaryInput.value = text;
                temporaryInput.setAttribute("readonly", "");
                temporaryInput.style.position = "fixed";
                temporaryInput.style.opacity = "0";
                document.body.append(temporaryInput);
                let copied;

                try {
                    temporaryInput.select();
                    copied = document.execCommand("copy");
                } finally {
                    temporaryInput.remove();
                }

                if (!copied) {
                    throw new Error("The browser did not allow copying to the clipboard.");
                }
            }

            label.textContent = "Command copied";
            copyStatus.textContent = "Ready to paste into your terminal.";
            window.setTimeout(() => {
                label.textContent = "Copy deploy command";
                copyStatus.textContent = "";
            }, 2800);
        } catch (error) {
            copyStatus.textContent = "Copy unavailable. Select and copy: python deploy.py";
            console.error("Unable to copy deploy command.", error);
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const content = document.querySelector("#content");

    async function swapContent(url, options = {}) {
        console.log("Fetching:", url); // log start
        try {
            const res = await fetch(url, options);
            const html = await res.text();

            const parser = new DOMParser();
            const doc = parser.parseFromString(html, "text/html");

            const newContent = doc.querySelector("#content");
            if (newContent) {
                content.innerHTML = newContent.innerHTML;
                console.log("Updated <main> content");
            }

            const finalURL = res.url;
            if (finalURL !== window.location.href) {
                history.pushState({}, "", finalURL);
                console.log("Updated URL:", finalURL);
            }

        } catch (err) {
            console.error("SPA nav failed:", err);
            window.location.href = url;
        }
    }

    document.querySelectorAll("[data-nav]").forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const url = link.getAttribute("href");
            swapContent(url);
        });
    });

    document.addEventListener("submit", (e) => {
        const form = e.target;
        if (form.hasAttribute("data-spa")) {
            e.preventDefault();

            const formData = new FormData(form);
            swapContent(form.action, {
                method: form.method,
                body: formData,
                headers: { "X-Requested-With": "fetch" }
            });
        }
    });

    window.addEventListener("popstate", () => {
        swapContent(location.pathname);
    });
});
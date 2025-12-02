async function getOrders() {
    try {
        const response = await fetch("http://localhost:8000/orders/",
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch");
        }

        const data = await response.json();
        return data;

    } catch (error) {
        console.error(error);
    }
}

async function getReviews() {
    try {
        const response = await fetch("http://localhost:8000/reviews/",
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch");
        }

        const data = await response.json();
        return data;

    } catch (error) {
        console.error(error);
    }
}
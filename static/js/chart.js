document.addEventListener("DOMContentLoaded", () => {
    try {
        // Fetch JSON data from the template
        const incomeDataElement = document.getElementById('income-data').textContent;
        const expenseDataElement = document.getElementById('expense-data').textContent;

        // Parse the JSON data
        const monthlyIncome = JSON.parse(incomeDataElement);
        const monthlyExpense = JSON.parse(expenseDataElement);

        // Map the data to labels and values for the chart
        const labels = monthlyIncome.map(data =>
            new Date(data.month).toLocaleString('default', { month: 'long', year: 'numeric' })
        );
        const incomeValues = monthlyIncome.map(data => data.total);
        const expenseValues = monthlyExpense.map(data => data.total);

        // Chart initialization
        const ctx = document.getElementById('income-expense-chart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Income',
                        data: incomeValues,
                        borderColor: 'green',
                        backgroundColor: 'rgba(0, 128, 0, 0.2)',
                    },
                    {
                        label: 'Expense',
                        data: expenseValues,
                        borderColor: 'red',
                        backgroundColor: 'rgba(255, 0, 0, 0.2)',
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                },
                scales: {
                    x: {
                        beginAtZero: true,
                    },
                    y: {
                        beginAtZero: true,
                    },
                },
            },
        });
    } catch (error) {
        console.error("Error parsing or displaying chart data:", error);
    }
});

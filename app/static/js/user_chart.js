// BAR_CHART
let user_bar_chart = document.getElementById("user_bar_chart")
new Chart(user_bar_chart, {
    type: "bar", 
    data: {
        labels: ["0-20", "20-40", "40-60", "60-80", "80-100"],
        datasets: [{
            label: "Score Distribution",
            data: score_list,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(201, 203, 207, 0.2)'
            ], 
            borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
                'rgb(201, 203, 207)'
            ],
            barThickness: 60,
            borderWidth: 1
        }
    ]
    }
})

// PIE_CHART

let user_pie_chart = document.getElementById("user_pie_chart")
new Chart(user_pie_chart, {
    type: "pie", 
    data: {
        labels: ["Attempted", "Not Attempted"],
        datasets: [{
            data: overall_list,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                // 'rgba(255, 159, 64, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                // 'rgba(54, 162, 235, 0.2)',
            ], 
            borderColor: [
                'rgb(255, 99, 132)',
                // 'rgb(255, 159, 64)',
                'rgb(75, 192, 192)',
                // 'rgb(54, 162, 235)',
            ],
            
            borderWidth: 1
        }]
    },
    options: {
        plugins: {
            legend: {
                position: "right"  
            }
        }
    }
})
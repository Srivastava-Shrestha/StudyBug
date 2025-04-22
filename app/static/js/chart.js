// BAR_CHART
let bar_chart = document.getElementById("bar_chart")
new Chart(bar_chart, {
    type: "bar", 
    data: {
        labels: ["Total Users", "Total Courses", "Average Chapters", "Total Quizzes"],
        datasets: [{
            label: "Overall Distribution",
            data: stats_list,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(54, 162, 235, 0.2)',
            ], 
            borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
            ],
            barThickness: 60,
            borderWidth: 1
        },
    {
        labels:["Total Users", "Total Courses", "Average Chapters", "Total Quizzes"],
        data: stats_list,
        label: "Trend",
        type: "line",
        borderColor: 'rgb(153, 102, 255)'
    }]
    }
})

// PIE_CHART

let pie_chart = document.getElementById("pie_chart")
new Chart(pie_chart, {
    type: "pie", 
    data: {
        labels: ["Attempted", "Not Attempted"],
        datasets: [{
            data: pie_list,
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
                position: "right"  // Moves legend to the right
            }
        }
    }
})



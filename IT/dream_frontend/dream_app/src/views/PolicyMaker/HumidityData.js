// import axios from "axios";

// let data1
// const getData = async () => {
//     await axios.get('https://').then(
//         resp => {
//             data1 = resp.data
//         }
//     )
// }

export const humidityData = {
    type: "bar",
    data: {
        labels: [
            '',
            'Adilabad',
            'Bhadradri Kothagudem',
            'Hanumakonda',
            'Hyderabad',
            'Jagtial',
            'Jangaon',
            'Jayashankar Bhupalpally',
            'Jogulamba Gadwal',
            'Kamareddy',
            'Karimnagar',
            'Khammam',
            'Kumuram Bheem',
            'Mahabubabad',
            'Mahabubnagar',
            'Mancherial',
            'Medak',
            'Medchal-Malkajgiri',
            'Mulugu',
            'Nagarkurnool',
            'Nalgonda',
            'Narayanpet',
            'Nirmal',
            'Nizamabad',
            'Peddapalli',
            'Rajanna Sircilla',
            'Rangareddy',
            'Sangareddy',
            'Siddipet',
            'Suryapet',
            'Vikarabad',
            'Wanaparthy',
            'Warangal',
            'Yadadri Bhuvanagiri'],
        datasets: [
            {   type: 'bar',
                label: "Humidity",
                data: [0, 0, 1, 2, 79, 82, 27, 14, 45, 4, 0, 0, 1, 2, 79, 82, 27, 14, 45, 4, 0, 0, 1, 2, 79, 100, 27, 14, 45, 4],
                backgroundColor: "rgba(54,73,93,.5)",
                borderColor: "#36495d",
                borderWidth: 3
            },
            {
                type: 'line',
                label: "Temperature",
                data: [50,50,50,50,50,50,50,5,50,50,50,50,50,50,50,80,50,50,80,50,50,50,40,50,50,50,50,50,50,50,7],
                backgroundColor: "red",
                borderColor: "red",
                borderWidth: 3,
            }
        ]
    },
    options: {
        responsive: true,
        lineTension: 0,
        scales: {
            y:{
                type: 'linear',
                position: 'left',
                min: 0,
                max: 100
            },

            y1: {
                type: 'linear',
                position: 'right',
                max: 60,
                min: 0,
                grid: {
                    drawOnChartArea: false,
                }
            }
        },
    },
};

export default humidityData;
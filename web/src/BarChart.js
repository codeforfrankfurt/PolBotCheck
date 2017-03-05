/**
 * Created by peter on 05.03.17.
 */
import React, {Component} from 'react';
import {Bar} from 'react-chartjs-2';

class BarChart extends Component {

  render() {
    let scores = [];
    let labels = [];
    this.props.topics.map((value) => {
      scores.push(value.score);
      labels.push(value.label)
    });

    const data = {
      labels: labels,
      datasets: [{
        label: 'Score',
        data: scores,
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(255, 159, 64, 0.2)'
        ],
        borderColor: [
          'rgba(255,99,132,1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)'
        ],
        borderWidth: 1
      }]
    };

    let options = {
      scales: {
        xAxes: [{
          stacked: true
        }],
        yAxes: [{
          stacked: true
        }]
      }
    };

    return (
      <div className={this.props.className}>
        <Bar data={data} options={options} width={600} height={250}/>
      </div>
    );
  }
}

export default BarChart;
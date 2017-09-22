import React, {Component} from 'react';
import {Pie} from 'react-chartjs-2';

class PieChart extends Component {

  render() {
    const data = {
      labels: ["Bots", "Menschen"],
      datasets: [{
        label: 'Verhältnis Bots / Menschen',
        data: [this.props.numbers.numBots,
          this.props.numbers.numHumans],
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

    return (
      <div className={this.props.className}>
        <Pie data={data} width={600} height={250}/>
      </div>
    );
  }
}

export default PieChart;

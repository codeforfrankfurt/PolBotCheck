import React, { Component } from 'react';

class PieChart extends Component {
    render() {
        return (
            <div className={this.props.className}>
                <img src="https://upload.wikimedia.org/wikipedia/commons/2/2b/Tortendiagramm_Themen_Pabst.jpg" />
            </div>
        );
    }
}

export default PieChart;

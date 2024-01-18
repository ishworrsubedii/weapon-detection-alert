import React from "react";
import { ResponsiveLine } from "@nivo/line";

const Dashboard = () => {
    const lineChartData = [
        {
            id: "Count",
            data: [
                { x: "2022-01-01", y: 10 },
                { x: "2022-01-02", y: 15 },
                { x: "2022-01-03", y: 8 },
                { x: "2022-01-04", y: 12 },
                { x: "2022-01-05", y: 5 },
            ],
        },
    ];

    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '800px', width: '600px' }}>
            <div style={{ height: '400px', width: '100%', display: 'grid', placeItems: 'center' }}>
                <h1>Weapon Detection</h1>
    
                <h2>Line Chart</h2>
                <div style={{ height: "400px" }}>
                    <ResponsiveLine
                        data={lineChartData}
                        margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
                        xScale={{ type: "time", format: "%Y-%m-%d", precision: "day" }}
                        xFormat="time:%Y-%m-%d"
                        yScale={{ type: "linear", min: "auto", max: "auto", stacked: true, reverse: false }}
                        axisTop={null}
                        axisRight={null}
                        axisBottom={{
                            format: "%b %d",
                            tickValues: "every 1 day",
                            legend: "Date",
                            legendOffset: 36,
                            legendPosition: "middle",
                        }}
                        axisLeft={{
                            legend: "Count",
                            legendOffset: -40,
                            legendPosition: "middle",
                        }}
                        enableGridX={false}
                        enableGridY={false}
                    />
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
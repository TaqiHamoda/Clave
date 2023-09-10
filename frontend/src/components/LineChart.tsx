import React from 'react';
import Chart from 'chart.js/auto';
import { Line } from 'react-chartjs-2';
import zoomPlugin from 'chartjs-plugin-zoom';
import { interpolateSpectral } from 'd3-scale-chromatic';
import {
    Box,
    BoxProps
} from '@chakra-ui/react';

Chart.register(zoomPlugin);

interface LineChartProps extends BoxProps {
    xLabel: string,
    yLabel: string,
    xData: number[],
    yLabels: string[],
    yDatasets: number[][],
}

export const LineChart = (props: LineChartProps) => {
    const { xLabel, yLabel, xData, yLabels, yDatasets, ...rest } = props;

    return <Box {...rest}>
        <Line
            data={{
                labels: xData,
                datasets: yDatasets.map((value, i) => {
                    return {
                        label: yLabels[i],
                        data: value,
                        borderColor: interpolateSpectral(i / yDatasets.length),
                        backgroundColor: interpolateSpectral(i / yDatasets.length)
                    };
                })
            }}
            options={{
                spanGaps: true,  // For Perfomance Enhancements
                animation: false,  // For Perfomance Enhancements
                transitions: {  // For Perfomance Enhancements
                    zoom: {
                        animation: {
                            duration: 0
                        }
                    }
                },
                plugins: {
                    zoom: {
                        pan: {
                            enabled: true,
                            mode: 'xy'
                        },
                        zoom: {
                            wheel: {
                                enabled: true,
                            },
                            pinch: {
                                enabled: true
                            },
                            mode: 'xy',
                        },
                    },
                    legend: {
                        labels: {
                            font: {
                                size: 14
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        type: 'linear',
                        title: {
                            display: true,
                            text: xLabel,
                            font: {
                                size: 18
                            }
                        }
                    },
                    y: {
                        type: 'linear',
                        title: {
                            display: true,
                            text: yLabel,
                            font: {
                                size: 18
                            }
                        }
                    }
                }
            }} />
    </Box>;
}
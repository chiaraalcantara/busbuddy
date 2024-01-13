// import React from 'react';
import { Collapse, Timeline } from "antd";


const Map = () => {
    const { Panel } = Collapse; 

    const busRoutes = [
        { 
            name: 'Bus 23',
            stops : [
                {
                    label: 'Bus Stop 1',
                    children: 'Dundas and Dufferin',
                },
                {
                    label: 'Bus Stop 2',
                    children: 'Dundas and Ossington',
                },
                {
                    label: 'Bus Stop 3',
                    children: 'Dundas and Bathurst',
                },
                {
                    label: 'Bus Stop 4',
                    children: 'Dundas and Spadina',
                },
                {
                    label: 'Bus Stop 5',
                    children: 'Dundas and University',
                },
            ]
        },
        {
            name: 'Bus 69',
            stops: [
                {
                    label: 'Bus Stop 1',
                    children: 'Steeles and Dufferin',
                },
                {
                    label: 'Bus Stop 2',
                    children: 'Steeles and Bathust',
                },
                {
                    label: 'Bus Stop 3',
                    children: 'Steeles and Yonge',
                },
                {
                    label: 'Bus Stop 4',
                    children: 'Steeles and Victoria Park',
                },
                {
                    label: 'Bus Stop 5',
                    children: 'Steeles and Kennedy',
                },
            ]
        },
        { 
            name: 'Bus 323',
            stops: [
                {
                    label: 'Bus Stop 1',
                    children: 'White Oaks',
                },
                {
                    label: 'Bus Stop 2',
                    children: 'Glenforest',
                },
                {
                    label: 'Bus Stop 3',
                    children: 'Bloor',
                },
                {
                    label: 'Bus Stop 4',
                    children: 'Trafalgar',
                },
                {
                    label: 'Bus Stop 4',
                    children: 'Earl Haig',
                },
            ]
        },
    ];

    
    return (
        <section className="map section">
            <div className="flex flex-col items-center justify-center ">
                <h1 className="text-lg font-semibold">Bus Routes</h1>
                {/* <ul className="flex flex-col">
                    {busRoutes.map((route) => (
                        <li key={route.id}>{route.name}</li>
                    ))} 
                </ul> */}
                <Collapse
                    size="large"
                    defaultActiveKey={['0']}
                    className="w-1/2"
                    ghost
                >
                    {busRoutes.map((route, index) => (
                        <Panel 
                            className="hover:bg-gray-100 hover:scale-105 transition duration-300 ease-in-out hover:shadow-lg"
                            header={route.name} 
                            key={index}
                            >
                            <Timeline
                                mode={index % 2 === 0 ? 'left' : 'right'}
                                items={route.stops}
                            />
                        </Panel>
                    ))}
                </Collapse>;
            </div>
        </section>
          
    );
};

export default Map;

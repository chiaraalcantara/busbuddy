// import React from 'react';
import { Collapse, Timeline } from "antd";
import { busRoutes } from "../../utils/constants";

const Map = () => {
    const { Panel } = Collapse; 

    return (
        <section className="map section">
            <div className="flex flex-col items-center justify-center ">
                <h1 className="text-3xl font-semibold mb-4">Bus Routes</h1>
                <h1 className="mb-4"> A list of bus routes that gets students to their schools, all busses leave at 6:45 am EST!</h1>
                <Collapse
                    size="large"
                    defaultActiveKey={['0']}
                    className="w-1/2"
                    ghost
                >
                    {busRoutes.map((route, index) => (
                        <Panel 
                        //hover:bg-gray-100
                            // change the styling here
                            className="hover:bg-gray-400 transition duration-300 ease-in-out hover:shadow-lg"
                            header={route.name} 
                            key={index}
                            >
                            <Timeline
                                mode={index % 2 === 0 ? 'left' : 'right'}
                                items={route.stops}
                            />
                        </Panel>
                    ))}
                </Collapse>
            </div>
        </section>
    );
};

export default Map;

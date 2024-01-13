// import React from 'react';

const BusListPage = () => {
    const busRoutes = [
        { id: 1, name: 'Route 1' },
        { id: 2, name: 'Route 2' },
        { id: 3, name: 'Route 3' },
        // Add more bus routes as needed
    ];

    return (
        <section className="map section">
            <div className="flex flex-col items-center justify-center ">
                <h1 className="text-lg font-semibold">Bus Routes</h1>
                <ul className="flex flex-col">
                    {busRoutes.map((route) => (
                        <li key={route.id}>{route.name}</li>
                    ))}
                </ul>
            </div>
        </section>
          
    );
};

export default BusListPage;

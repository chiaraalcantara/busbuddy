export const busRoutes = [
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
        name: 'Bus 29',
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

export const busNames = busRoutes.map((route) => route.name);
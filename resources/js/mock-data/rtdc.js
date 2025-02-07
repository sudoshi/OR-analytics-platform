// Updated mock data for Real-Time Demand and Capacity features

// System Capacity Assessment Data
export const systemCapacityData = {
    overview: {
        availableBeds: 15,
        expectedDC: 31,
        pendingRequests: 37,
        criticalUnits: 4
    },
    bedDistribution: {
        zeroBeds: 4,
        oneBed: 4,
        twoPlusBeds: 4
    },
    units: [
        {
            id: 1,
            name: '5 East',
            description: 'Cardiology / Tele',
            availableBeds: 1,
            predictedDC: 3,
            targetedRequests: 4,
            status: 0,
            redStretchPlan: 'Expediting 2 telemetry discharges with cardiology team'
        },
        {
            id: 2,
            name: '5 West',
            description: 'Nephrology',
            availableBeds: 2,
            predictedDC: 1,
            targetedRequests: 2,
            status: 1
        },
        {
            id: 3,
            name: '6 East',
            description: 'Orthopedics',
            availableBeds: 0,
            predictedDC: 4,
            targetedRequests: 3,
            status: 1
        },
        {
            id: 4,
            name: '6 West',
            description: 'Oncology',
            availableBeds: 4,
            predictedDC: 1,
            targetedRequests: 2,
            status: 3
        },
        {
            id: 5,
            name: '7 East',
            description: 'General Surgery',
            availableBeds: 1,
            predictedDC: 5,
            targetedRequests: 4,
            status: 2
        },
        {
            id: 6,
            name: '7 West',
            description: 'Pulmonology',
            availableBeds: 0,
            predictedDC: 2,
            targetedRequests: 4,
            status: -2,
            redStretchPlan: 'Moving stable patients to med/surg to create pulmonary beds'
        },
        {
            id: 7,
            name: '8 East',
            description: 'Neurology',
            availableBeds: 2,
            predictedDC: 3,
            targetedRequests: 2,
            status: 3
        },
        {
            id: 8,
            name: '8 West',
            description: 'Internal Medicine',
            availableBeds: 1,
            predictedDC: 4,
            targetedRequests: 6,
            status: -1,
            redStretchPlan: 'Case management reviewing 3 potential discharges'
        },
        {
            id: 9,
            name: '9 East',
            description: 'General Surgery',
            availableBeds: 3,
            predictedDC: 2,
            targetedRequests: 1,
            status: 4
        },
        {
            id: 10,
            name: '9 West',
            description: 'Internal Medicine',
            availableBeds: 0,
            predictedDC: 3,
            targetedRequests: 3,
            status: 0
        },
        {
            id: 11,
            name: 'ICU',
            description: 'Intensive Care',
            availableBeds: 1,
            predictedDC: 2,
            targetedRequests: 4,
            status: -1,
            redStretchPlan: 'Expediting 2 step-downs to create critical care capacity'
        },
        {
            id: 12,
            name: 'CCU',
            description: 'Cardiac Care',
            availableBeds: 0,
            predictedDC: 1,
            targetedRequests: 2,
            status: -1,
            redStretchPlan: 'Transferring stable patient to 5E telemetry'
        }
    ]
};

// Census Data
export const censusData = {
    total: {
        bedTypes: {
            icu: {
                total: 50,
                occupied: 42,
                pending: 3,
            },
            medical: {
                total: 120,
                occupied: 98,
                pending: 5,
            },
            surgical: {
                total: 80,
                occupied: 65,
                pending: 4,
            },
            pediatric: {
                total: 40,
                occupied: 28,
                pending: 2,
            },
            obstetrics: {
                total: 30,
                occupied: 25,
                pending: 1,
            },
        },
    },
};

// Department Data (preserved)
export const departmentData = {
    // ... (existing content)
};

// **Updated Staffing Data**
export const staffingData = {
    currentShift: {
        present: 45,
        required: 50,
        coverage: 90,
        skillMix: {
            nurses: { present: 25, required: 28 },
            techs: { present: 12, required: 14 },
            support: { present: 8, required: 8 },
        },
    },
    nextShift: {
        scheduled: 48,
        required: 50,
        predicted: 52,
        skillMix: {
            nurses: { scheduled: 27, required: 28 },
            techs: { scheduled: 13, required: 14 },
            support: { scheduled: 8, required: 8 },
        },
    },
    trends: {
        daily: [
            { date: '2025-02-01', coverage: 92 },
            { date: '2025-02-02', coverage: 88 },
            { date: '2025-02-03', coverage: 95 },
            // ... more trend data
        ],
    },
};

// **Updated Alerts Data**
export const alertsData = {
    active: [
        {
            id: 1,
            priority: 'high',
            title: 'Critical Staffing Shortage',
            description: 'ICU requires additional nursing coverage for night shift',
            department: 'ICU',
            time: '10 mins ago',
            category: 'staffing',
            actions: ['View Schedule', 'Contact Pool'],
        },
        {
            id: 2,
            priority: 'medium',
            title: 'High Bed Occupancy',
            description: 'Medical ward occupancy exceeds 90%',
            department: 'Medical Ward',
            time: '20 mins ago',
            category: 'capacity',
            actions: ['Reassign Patients', 'Activate Surge Plan'],
        },
        {
            id: 3,
            priority: 'low',
            title: 'Equipment Maintenance Due',
            description: 'Routine check for ventilators in Respiratory Unit',
            department: 'Respiratory Unit',
            time: '1 hour ago',
            category: 'service',
            actions: ['Schedule Maintenance'],
        },
        // ... more alerts
    ],
    statistics: {
        byPriority: {
            high: 2,
            medium: 3,
            low: 1,
        },
    },
};

// Service Definitions (preserved)
export const services = [
    // ... existing services
];

// Service Categories (preserved)
export const serviceCategories = {
    // ... existing categories
};

// Generate Demo Data Function (preserved)
export const generateDemoData = () => {
    // ... existing function
};

// Unit Services Data (preserved)
export const unitServicesData = generateDemoData();

// Capacity Timeline Data
export const capacityTimelineData = {
    demandCapacity: {
        overnight: {
            labels: ['2 PM', '4 PM', '6 PM', '8 PM', '10 PM', '12 AM', '2 AM', '4 AM', '6 AM', '8 AM'],
            datasets: [
                {
                    label: 'Predicted Demand',
                    data: [480, 485, 490, 488, 485, 482, 478, 475, 472, 470],
                    borderColor: 'rgb(var(--color-healthcare-warning))',
                    backgroundColor: 'rgba(var(--color-healthcare-warning), 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Available Capacity',
                    data: [485, 488, 492, 495, 490, 488, 485, 482, 480, 478],
                    borderColor: 'rgb(var(--color-healthcare-primary))',
                    backgroundColor: 'rgba(var(--color-healthcare-primary), 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        morning: {
            labels: ['8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM'],
            datasets: [
                {
                    label: 'Predicted Demand',
                    data: [470, 472, 475, 478, 480, 482, 485],
                    borderColor: 'rgb(var(--color-healthcare-warning))',
                    backgroundColor: 'rgba(var(--color-healthcare-warning), 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Available Capacity',
                    data: [478, 480, 482, 485, 488, 490, 492],
                    borderColor: 'rgb(var(--color-healthcare-primary))',
                    backgroundColor: 'rgba(var(--color-healthcare-primary), 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        }
    },
    discharges: [
        {
            id: 1,
            unit: '5E',
            room: '5E-12',
            priority: 'high',
            expectedTime: '10:00 AM',
            milestones: [
                { id: 1, name: 'MD Order', status: 'completed' },
                { id: 2, name: 'Case Mgmt', status: 'completed' },
                { id: 3, name: 'Transport', status: 'in_progress' },
                { id: 4, name: 'Pharmacy', status: 'pending' },
                { id: 5, name: 'Final Check', status: 'pending' }
            ],
            notes: 'Telemetry discharge, coordinating with cardiology'
        },
        {
            id: 2,
            unit: 'ICU',
            room: 'ICU-04',
            priority: 'high',
            expectedTime: '11:30 AM',
            milestones: [
                { id: 1, name: 'MD Order', status: 'completed' },
                { id: 2, name: 'Case Mgmt', status: 'in_progress' },
                { id: 3, name: 'Transport', status: 'blocked' },
                { id: 4, name: 'Pharmacy', status: 'pending' },
                { id: 5, name: 'Final Check', status: 'pending' }
            ],
            notes: 'Step-down to medical floor pending bed availability'
        }
    ],
    huddles: [
        {
            id: 1,
            unit: 'ICU',
            status: 'critical',
            currentOccupancy: '95%',
            predictedDemand: 4,
            availableBeds: 1,
            redStretchPlan: {
                actions: [
                    'Expedite 2 step-downs to medical floor',
                    'Review 3 potential early discharges',
                    'Coordinate with ED for incoming critical patients'
                ],
                responsibleParty: 'Dr. Johnson',
                deadline: '10:30 AM'
            }
        },
        {
            id: 2,
            unit: 'Medical Floor',
            status: 'warning',
            currentOccupancy: '88%',
            predictedDemand: 6,
            availableBeds: 3,
            redStretchPlan: {
                actions: [
                    'Prioritize 4 pending discharges',
                    'Coordinate with case management for placement',
                    'Review bed assignments for optimization'
                ],
                responsibleParty: 'Charge RN Smith',
                deadline: '11:00 AM'
            }
        }
    ],
    executiveReport: {
        summary: {
            dischargeTarget: { value: '85%', trend: 5, description: '52/61 completed' },
            bedUtilization: { value: '92%', trend: -2, description: 'Peak at 2 PM' },
            avgLOS: { value: '4.2', trend: -8, description: 'Days per patient' },
            redPlans: { value: '6', trend: null, description: 'Executed today' }
        },
        improvements: [
            {
                id: 1,
                title: 'Transport Coordination',
                status: 'in_progress',
                impact: 'High',
                metrics: 'Reduced delays by 15 min',
                owner: 'Transport Team'
            },
            {
                id: 2,
                title: 'Early Discharge Planning',
                status: 'completed',
                impact: 'Medium',
                metrics: '+12% before noon',
                owner: 'Case Management'
            }
        ],
        delays: {
            labels: ['Transport', 'Pharmacy', 'Cleaning', 'Documentation', 'Other'],
            datasets: [{
                label: 'Delays',
                data: [45, 30, 25, 20, 15],
                backgroundColor: [
                    'rgba(var(--color-healthcare-primary), 0.8)',
                    'rgba(var(--color-healthcare-secondary), 0.8)',
                    'rgba(var(--color-healthcare-success), 0.8)',
                    'rgba(var(--color-healthcare-warning), 0.8)',
                    'rgba(var(--color-healthcare-info), 0.8)'
                ],
                borderWidth: 0
            }]
        }
    }
};

// Ancillary Services Timeline Data (preserved)
export const serviceTimelines = {
    hourly: [
        // ... existing content
    ],
    daily: [
        // ... existing content
    ],
};

// Exporting all data
export default {
    censusData,
    departmentData,
    staffingData,
    alertsData,
    services,
    serviceCategories,
    unitServicesData,
    serviceTimelines,
    capacityTimelineData,
};

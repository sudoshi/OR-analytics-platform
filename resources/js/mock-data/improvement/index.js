// Mock data exports for PDSA cycles
export const activePDSACycles = [
{
    id: 1,
    title: 'Reducing Wait Times',
    status: 'active',
    startDate: '2024-02-15',
    phase: 'Plan',
    description: 'Initiative to reduce patient wait times in emergency department',
    metrics: ['Average wait time', 'Patient satisfaction'],
    team: ['Dr. Smith', 'Nurse Johnson', 'Admin Wilson'],
    progress: 25
},
{
    id: 2,
    title: 'Medication Error Prevention',
    status: 'active', 
    startDate: '2024-01-30',
    phase: 'Do',
    description: 'Implementing new medication verification protocols',
    metrics: ['Error rate', 'Near-miss reports'],
    team: ['Dr. Jones', 'Pharmacist Brown'],
    progress: 50
},
{
    id: 3,
    title: 'Patient Discharge Process',
    status: 'active',
    startDate: '2024-02-01',
    phase: 'Study',
    description: 'Streamlining the discharge process to improve efficiency',
    metrics: ['Discharge time', 'Readmission rate'],
    team: ['Dr. Williams', 'Nurse Davis'],
    progress: 75
}
];

// Mock data for improvement opportunities
export const improvementOpportunities = [
  {
    id: 1,
    title: 'Sample Opportunity',
    description: 'This is a placeholder opportunity',
    status: 'active',
    priority: 'medium',
    createdAt: new Date().toISOString(),
  }
];

export const improvementStats = {
  totalOpportunities: 10,
  activeOpportunities: 5,
  completedOpportunities: 5,
  totalCycles: 3,
  activeCycles: 2,
  completedCycles: 1,
};

export const metrics = {
  total: 1,
  active: 1,
  completed: 0
};

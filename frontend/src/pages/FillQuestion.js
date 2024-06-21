import React, { useState } from 'react';
import "../styles/FillQuestion.css";
import { useNavigate } from 'react-router-dom';
import Logo from "../assets/photos/brig.png"


function FillQuestion() {
    const [formData, setFormData] = useState({
        "Age (yrs)": 0,
        "Weight (Kg)": 0,
        "Height(Cm)": 0,
        "Pulse rate(bpm)": 0,
        "RR (breaths/min)": 0,
        "Cycle(R/I)": 0,
        "Cycle length(days)": 0,
        "Marraige Status (Yrs)": 0,
        "Pregnant(Y/N)": 0,
        "No. of abortions": 0,
        "Hip(inch)": 0,
        "Waist(inch)": 0,
        "Waist:Hip Ratio": 0,
        "BP _Systolic (mmHg)": 0,
        "BP _Diastolic (mmHg)": 0,
    });
    const navigate = useNavigate();

    const handleInputChange = (e) => {
        const { id, value } = e.target;
        setFormData({ ...formData, [id]: value });
    };

    const handleContinueClick = () => {
        // Handle continue button click
        console.log(formData);
        // You can add your logic here, e.g., navigating to another page
        fetch('http://127.0.0.1:5000/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                navigate('/results', { state: { data } });
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    };

    const handleBackClick = () => {
        // Handle back button click
        navigate(-1); // This will navigate back to the previous page
    };

    return (
        <div className='question-screen'>
            <div className='frame'>
                <button className='back' onClick={handleBackClick}>Back</button>
                <img src={Logo} className='corner-logo'/>
                <div className='input-groups'>
                    <div className='row-1'>
                        <div className='input-group'>
                            <label htmlFor='age'>Age (yrs):</label>
                            <input
                                type='number'
                                id='Age (yrs)'
                                value={formData.age}
                                onChange={handleInputChange}
                                placeholder='Enter your age'
                            />
                        </div>
                        <div className='input-group'>
                            <label htmlFor='weight'>Weight (Kg):</label>
                            <input
                                type='number'
                                id='Weight (Kg)'
                                value={formData.weight}
                                onChange={handleInputChange}
                                placeholder='Enter your weight in Kg'
                            />
                        </div>
                        <div className='input-group'>
                            <label htmlFor='height'>Height (Cm):</label>
                            <input
                                type='number'
                                id='Height(Cm)'
                                value={formData.height}
                                onChange={handleInputChange}
                                placeholder='Enter your height in cm'
                            />
                        </div>
                        <div className='input-group'>
                            <label htmlFor='pulse'>Pulse rate (bpm):</label>
                            <input
                                type='number'
                                id='Pulse rate(bpm)'
                                value={formData.pulse}
                                onChange={handleInputChange}
                                placeholder='Enter your pulse in bpm'
                            />
                        </div>
                    </div>
                    <div className='row-2'>
                        <div className='input-group'>
                            <label htmlFor='rr'>Respiratory Rate (breaths/min):</label>
                            <input
                                type='number'
                                id='RR (breaths/min)'
                                value={formData.rr}
                                onChange={handleInputChange}
                                placeholder='Enter your respiratory rate in breaths/min'
                            />
                        </div>


                        <div className='input-group'>
                            <label htmlFor='cycleRI'>Cycle (R/I):</label>
                            <input
                                type='text'
                                id='Cycle(R/I)'
                                value={formData.cycleRI}
                                onChange={handleInputChange}
                                placeholder='Enter R or I'
                            />
                        </div>
                        <div className='input-group'>
                            <label htmlFor='cycleLength'>Cycle length (days):</label>
                            <input
                                type='number'
                                id='Cycle length(days)'
                                value={formData.cycleLength}
                                onChange={handleInputChange}
                                placeholder='Enter cycle length in days'
                            />
                        </div>
                        <div className='input-group'>
                            <label htmlFor='marriageStatus'>Marriage Status (Yrs):</label>
                            <input
                                type='number'
                                id='Marraige Status (Yrs)'
                                value={formData.marriageStatus}
                                onChange={handleInputChange}
                                placeholder='Enter years of marriage'
                            />
                        </div>
                    </div>
                    <div className='row-3'>
                        <div className='input-group'>
                            <label htmlFor='pregnant'>Pregnant (Y/N):</label>
                            <input
                                type='number'
                                id='Pregnant(Y/N)'
                                value={formData.pregnant}
                                onChange={handleInputChange}
                                placeholder='Enter 1 (Yes) or 0 (No)'
                            />
                        </div>

                        <div className='input-group'>
                            <label htmlFor='numberOfAbortions'>No. of abortions:</label>
                            <input
                                type='number'
                                id='No. of abortions'
                                value={formData.numberOfAbortions}
                                onChange={handleInputChange}
                                placeholder='Enter the number of abortions'
                            />
                        </div>


                        <div className='input-group'>
                            <label htmlFor='hip'>Hip (inch):</label>
                            <input
                                type='number'
                                id='Hip(inch)'
                                value={formData.hip}
                                onChange={handleInputChange}
                                placeholder='Enter hip size in inches'
                            />
                        </div>
                        <div className='input-group'>
                            <label htmlFor='waist'>Waist (inch):</label>
                            <input
                                type='number'
                                id='Waist(inch)'
                                value={formData.waist}
                                onChange={handleInputChange}
                                placeholder='Enter waist size in inches'
                            />
                        </div>
                    </div>
                    <div className='row-4'>
                        <div className='input-group'>
                            <label htmlFor='waistHipRatio'>Waist:Hip Ratio:</label>
                            <input
                                type='number'
                                id='Waist:Hip Ratio'
                                value={formData.waistHipRatio}
                                onChange={handleInputChange}
                                placeholder='Enter waist:hip ratio'
                            />
                        </div>
                        <div className='input-group'>
                            <label htmlFor='systolicBP'>Systolic Blood Pressure (mmHg):</label>
                            <input
                                type='number'
                                id='BP _Systolic (mmHg)'
                                value={formData.systolicBP}
                                onChange={handleInputChange}
                                placeholder='Enter your systolic BP in mmHg'
                            />
                        </div>  
                        <div className='input-group'>
                            <label htmlFor='diastolicBP'>Diastolic Blood Pressure (mmHg):</label>
                            <input
                                type='number'
                                id='BP _Diastolic (mmHg)'
                                value={formData.diastolicBP}
                                onChange={handleInputChange}
                                placeholder='Enter your diastolic BP in mmHg'
                            />
                        </div>
                        <div className='input-group'>
                        </div>

                    </div>
                    
                </div>
                <div className='button-frame'>
                    <button className='continue-button' onClick={handleContinueClick}>
                        {'View Results'}
                    </button>
                </div>
            </div>
        </div>

    );
}

export default FillQuestion;

import styled from '@emotion/styled'
import React from 'react'

interface Option {
    label: string,
    click: ()=>void,
}

export interface FloatOptionsProps {
    x: number,
    y: number,
    visible: boolean,
    onCancel?: ()=>void,
    options: Option[]
}

const FloatOptions: React.FC<FloatOptionsProps> = ({x, y, visible, onCancel, options}) => {
    const DivStyled = styled.div`
        left: ${x}px;
        top: ${y}px;
    `

    const handleCancel = () => {
        if (onCancel) {
            onCancel();
        }
    }
  return (
    <>
        {visible && 
            <div className='absolute w-screen h-screen' onClick={handleCancel}>
                <DivStyled className='absolute bg-slate-50 rounded p-1 shadow-md'>
                    {options.map(({label, click}, index)=>(
                        <div key={index} className='hover:bg-slate-200 cursor-pointer w-full p-1' onClick={click}>
                            {label}
                        </div>
                    ))}
                </DivStyled>
            </div>
        }
    </>
  )
}

export default FloatOptions
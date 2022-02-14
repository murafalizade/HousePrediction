import React, { useState,useEffect } from 'react';
import {cities,regions} from '../data'
import axios from 'axios'

export default function PredictForm() {
  const [price, setPrcie] = useState<number>(0)
  const [types, setTypes] = useState<string>('Alış')
  const [cat, setCat] = useState<string>('Mənzil')
  const [city, setCity] = useState<string>('')
  const [region, setRegion] = useState<string>('')
  const [room, setRoom] = useState<number | undefined>()
  const [floor, setFloor] = useState<number | undefined>()
  const [allFloor, setAllFloor] = useState<number | undefined>()
  const [area, setArea] = useState<number>()

  const compute = async (e: any) => {
    e.preventDefault()
    setPrcie(0)
    console.log(area, allFloor, room, floor, cat, city, types, region);
    const result = await axios.post('/api/v1/predict',{area, allFloor, room, floor, cat, city, types, region});
    console.log(result.data.toString().length,cat);
    types==='kiraye' && result.data.toString().length>4?setPrcie(parseInt(result.data)/30):setPrcie(parseInt(result.data))
  }

  useEffect(()=>{
    if(cat==='ev'){
      setAllFloor(0);
      setFloor(0);
    }
  },[cat])
  return (
    <>
      <form>
        <div className='row first'>
          <select value={types} onChange={(e: any) => setTypes(e.target.value)}>Alış
            <option value={'alis'}>Alış</option>
            <option value={'kiraye'}>Kirayə</option>
          </select>
          <select value={cat} onChange={(e: any) => setCat(e.target.value)}>Mənzil
            <option value={'menzil'}>Mənzil</option>
            <option value={'yeni_tikili'}>Yeni tikili</option>
            <option value={'kohne_tikili'}>Köhnə tikili</option>
            <option value={'ev'}>Ev/Villa</option>
          </select>
          <select value={room} onChange={(e: any) => setRoom(e.target.value)} required >Otaq sayı
            <option value={1}>Otaq sayı</option>
            <option value={1}>1 otaqlı </option>
            <option value={2}>2 otaqlı </option>
            <option value={3}>3 otaqlı </option>
            <option value={4}>4 otaqlı </option>
            <option value={5}>5 otaq və daha çox</option>
          </select>
        </div>
        <div className='row second'>
          <select value={city} onChange={(e: any) => setCity(e.target.value)}>Şəhər
            <option>İstənilən şəhər</option>
            {cities.map((cit:string,index:number)=>(<option key={index} value={cit}>{cit}</option>))}
          </select>
          <select value={region} onChange={(e: any) => setRegion(e.target.value)} disabled={city !== 'Bakı' ? true : false}>Rayon və qəsəbə
            <option>Rayon və qəsəbə</option>
            {regions.map((reg:string,index:number)=>(
              <option key={index} value={reg}>{reg}</option>
            ))}
          </select>
        </div>
        <div className='row thrid'>
          <input value={area} onChange={(e: any) => setArea(e.target.value)} placeholder='Sahə, m²' />
          {cat === 'ev' ? null : (<>
            <input value={allFloor} onChange={(e: any) => setAllFloor(e.target.value)} placeholder='Ümumi mərtəbə' />
            <input value={floor} onChange={(e: any) => setFloor(e.target.value)} placeholder='Yerləşdiyi mərtəbə' />
          </>)}
        </div>

        <button onClick={(e: any) => compute(e)} className='sumbitBtn'>Hesabla</button>
      </form>
      {!price ? null : (<p className='result'><b>Qiymət: </b><span>{price.toFixed(2)} AZN{types==='kiraye'?'/Ay':null}</span></p>)}

    </>
  );
}

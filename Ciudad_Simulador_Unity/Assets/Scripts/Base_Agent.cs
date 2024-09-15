using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public abstract class Base_Agent:MonoBehaviour
{
    public int id;
    public Vector3 pos;
    public string tipo;
    public string estado;

    public void CreateAgent(int _id, Vector3 _pos, string _tipo, string _estado)
    {
        id = _id;
        pos = _pos * 5;
        tipo = _tipo;
        transform.position = pos;
        estado = _estado;
    }

    public void SetPosition(Vector3 _pos,string state)
    {
        pos = _pos * 5;
        estado = state;
    }
}

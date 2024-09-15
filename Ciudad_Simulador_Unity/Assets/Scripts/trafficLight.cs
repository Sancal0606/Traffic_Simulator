using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class trafficLight : Base_Agent
{
    [SerializeField] Material red;
    [SerializeField] Material orange;
    [SerializeField] Material green;

    [SerializeField] GameObject circle;

    private void Update()
    {
        switch (estado)
        {
            case ("rojo"):
                circle.GetComponent<MeshRenderer>().material = red;
                break;
            case ("naranja"):
                circle.GetComponent<MeshRenderer>().material = orange;
                break;
            case ("verde"):
                circle.GetComponent<MeshRenderer>().material = green;
                break;
        }
        
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour
{
    [SerializeField] float cameraRotSpeedHorz;
    [SerializeField] float cameraRotSpeedVert;
    float horz;
    float vert;

    // Update is called once per frame
    void Update()
    {
        horz = Input.GetAxis("Horizontal");
        vert = Input.GetAxis("Vertical");
        

        transform.Rotate(0, 
            -horz * cameraRotSpeedHorz * Time.deltaTime, 0.0f, Space.Self);
    }
}

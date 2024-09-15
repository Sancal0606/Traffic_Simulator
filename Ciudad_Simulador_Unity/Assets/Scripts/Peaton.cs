using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Peaton : Base_Agent
{
    [SerializeField] private float speed;

    private Vector3 dir;
    [SerializeField] private float rotSpeed;


    void Update()
    {
        dir = (pos - transform.position).normalized;
        if (Vector3.Distance(pos, transform.position) < 0.2f)
        {
            dir = (pos - transform.position).normalized;
            return;
            //animController.SetBool("isMoving", false);
        }
        else
        {
            //animController.SetBool("isMoving", true);
        }




        Vector3 direction = Vector3.RotateTowards(transform.forward, dir, rotSpeed * Time.deltaTime, 0);
        transform.rotation = Quaternion.LookRotation(direction);
        transform.position += dir * speed * Time.deltaTime;
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarMovement : Base_Agent
{
    [SerializeField] private float speed;

    private Vector3 dir;
    [SerializeField] private float rotSpeed;
    [SerializeField] private ParticleSystem dustParticles;


    void Update()
    {
        dir = (pos - transform.position).normalized;
        if (Vector3.Distance(pos, transform.position) < 0.2f)
        {
            return;
        }

        
        if (Vector3.Distance(dir,transform.forward.normalized) >= 0.2f)
        {
            dustParticles.Stop();
        }
        
        if(Vector3.Distance(dir, transform.forward.normalized) < 0.2f)
        {
            if (!dustParticles.isPlaying)
            {
                dustParticles.Play();
            }
        }

        Vector3 direction = Vector3.RotateTowards(transform.forward, dir, rotSpeed * Time.deltaTime, 0);
        transform.rotation = Quaternion.LookRotation(direction);
        transform.position += dir * speed * Time.deltaTime;
    }
}
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SmoothCameraFollow : MonoBehaviour
{
    
    [SerializeField] private Transform target;  // Object to follow
    [SerializeField] private float smoothSpeed = 0.1f;
    [SerializeField] private Vector3 offset;  // Distance from the target
    

    // Update is called once per frame
    void FixedUpdate()
    {
        Vector3 desiredPosition = target.position + offset;
        if (target.position.y <= 0f)
        {
            desiredPosition.y -= target.position.y;
        }

        if (target.position.x <= 0f)
        {
            desiredPosition.x -= target.position.x;
        }
        
        Vector3 smoothedPosition = Vector3.Lerp(transform.position, desiredPosition, smoothSpeed);
        transform.position = smoothedPosition; 
    }
}

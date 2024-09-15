using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System;
using UnityEngine.UI;
using TMPro;

public class GameManager : MonoBehaviour
{
    public Dictionary<int,GameObject> dicAgents;
    private List<GameObject> allAgents;
    public static GameManager instance;
    public GameObject car;
    public GameObject peaton;
    public GameObject trafficLight;
    public GameObject camion;
    public GameObject carroReactivo;
    public GameObject dog;
    public float timeBtwnSteps;
    float countdown;
    bool isSimulating;
    public GameObject menu;

    [SerializeField] private TMP_InputField carrosRec, carrosInt, perros, camiones, peatones;



    [Serializable]
    struct DataCiudad
    {
        public string NUM_CARROS_REACTIVOS;
        public string NUM_CARROS_INTELIGENTES;
        public string NUM_AUTOBUSES;
        public string NUM_PEATONES;
        public string NUM_PERROS;
    };

    [Serializable]
    public struct Agent
    {
        public int id;
        public string tipo;
        public int x;
        public int y;
        public string estado;
    };


    [Serializable]
    struct Simulation
    {
        public List<Agent> agents;
    };

    private void Start()
    {
        instance = this;
        countdown = timeBtwnSteps;
        isSimulating = false;
        allAgents = new List<GameObject>();
        //yield return InitializeSimulation();
        //yield return GetFirstStep();
    }

    private void Update()
    {
        if (countdown <= 0 & isSimulating)
        {
            StartCoroutine(GetStep());
            countdown = timeBtwnSteps;
        }
        countdown -= Time.deltaTime;
    }

    

    private IEnumerator InitializeSimulation()
    {
        DataCiudad postData = new DataCiudad();
        postData.NUM_CARROS_REACTIVOS = carrosRec.text;
        postData.NUM_CARROS_INTELIGENTES = carrosInt.text;
        postData.NUM_PEATONES = peatones.text;
        postData.NUM_PERROS = perros.text;
        postData.NUM_AUTOBUSES = camiones.text;

        string JSON = JsonUtility.ToJson(postData);

        string contenType = "application/json";
        string url = "http://127.0.0.1:5000/crear-ciudad";
        using (UnityWebRequest postRequest = UnityWebRequest.Post(url, JSON, contenType))
        {
            yield return postRequest.SendWebRequest();
            if (postRequest.result == UnityWebRequest.Result.Success)
            {
                Debug.Log("Yei");
                StartCoroutine(GetFirstStep());
            }
            else
            {
              
            }
        }
    }

    IEnumerator GetFirstStep()
    {
        string url = "http://127.0.0.1:5000/step";

        using (UnityWebRequest getRequest = UnityWebRequest.Get(url))
        {
            yield return getRequest.SendWebRequest();

            if (getRequest.result == UnityWebRequest.Result.Success)
            {
                string response = getRequest.downloadHandler.text;
                Simulation simulationData = JsonUtility.FromJson<Simulation>(response);
                Debug.Log(response);
                Debug.Log("H");
                CreateAgents(simulationData);
                isSimulating = true;
                
            }
            else
            {
                Debug.Log("Error with the server comunication");
            }
        }
    }

    void CreateAgents(Simulation simulationData)
    {
        dicAgents = new Dictionary<int, GameObject>();
        Vector3 tempPos = new Vector3(0,0,0);
        Debug.Log(simulationData.agents.Count);
        
        foreach (Agent agent in simulationData.agents)
        {
            
            tempPos.x = agent.x;
            tempPos.z = agent.y;
            GameObject temp = null;
           
            switch (agent.tipo)
            {
                case ("Peaton"):
                    temp = Instantiate(peaton, tempPos, Quaternion.identity);
                    break;
                case ("CarroInteligente"):
                    temp = Instantiate(car, tempPos, Quaternion.identity);
                    break;
                case ("Semaforo"):
                    temp = Instantiate(trafficLight, tempPos, Quaternion.identity);
                    break;
                case ("Autobus"):
                    temp = Instantiate(camion, tempPos, Quaternion.identity);
                    break;
                case ("CarroReactivo"):
                    temp = Instantiate(carroReactivo, tempPos, Quaternion.identity);
                    break;
                case ("Perro"):
                    temp = Instantiate(dog, tempPos, Quaternion.identity);
                    break;

            }
            Debug.Log("h");
            temp.GetComponent<Base_Agent>().CreateAgent(agent.id, tempPos, agent.tipo,agent.estado);
            allAgents.Add(temp);
            dicAgents.Add(agent.id, temp);
            

        }
    }

    void UpdateAgents(Simulation simulationData)
    {
        Vector3 tempPos = new Vector3(0, 0, 0);
        foreach (Agent agent in simulationData.agents)
        {
            tempPos.x = agent.x;
            tempPos.z = agent.y;
            dicAgents[agent.id].GetComponent<Base_Agent>().SetPosition(tempPos,agent.estado);

        }
    }

    IEnumerator GetStep()
    {
        string url = "http://127.0.0.1:5000/step";

        using (UnityWebRequest getRequest = UnityWebRequest.Get(url))
        {
            yield return getRequest.SendWebRequest();

            if (getRequest.result == UnityWebRequest.Result.Success)
            {
                string response = getRequest.downloadHandler.text;
                Simulation simulationData = JsonUtility.FromJson<Simulation>(response);
                foreach (Agent agent in simulationData.agents)
                {
                    UpdateAgents(simulationData);
                }
            }
            else
            {
                Debug.Log("Error with the server comunication");
            }
        }
    }

    public void Restart()
    {
        dicAgents = dicAgents = new Dictionary<int, GameObject>();
        foreach (GameObject agent in allAgents)
        {
            Destroy(agent);
        }
        StartCoroutine(InitializeSimulation());
        menu.SetActive(false);
        
    }

    public void ChangeMenu()
    {
        menu.SetActive(!menu.activeSelf);
    }
}

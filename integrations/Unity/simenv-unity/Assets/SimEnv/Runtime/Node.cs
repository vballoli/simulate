using UnityEngine;

namespace SimEnv {
    public class Node : MonoBehaviour {
        public void Initialize() {
            Simulator.Register(this);
        }
    }
}
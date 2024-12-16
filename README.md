# Biased Simulations Analysis and Free Energy Reconstruction

This repository provides a system for analyzing biased simulations and reconstructing potential of mean force (PMF) and free energy (ΔG) profiles for various reaction coordinates. Below is a description of the repository structure and the functionalities provided.

The example system here is based on: https://doi.org/10.1371/journal.pone.0267155
Korolainen, H., Lolicato, F., Enkavi, G., Pérez-Gil, J., Kulig, W., & Vattulainen, I. (2022). Dimerization of the pulmonary surfactant protein C in a membrane environment. *PLOS ONE*, 17(4), e0267155. [https://doi.org/10.1371/journal.pone.0267155](https://doi.org/10.1371/journal.pone.0267155)

The method is dscribed in:
Enkavi, G., Mikkolainen, H., Güngör, B., Ikonen, E., & Vattulainen, I. (2017). Concerted regulation of NPC2 binding to endosomal/lysosomal membranes by bis(monoacylglycero)phosphate and sphingomyelin. *PLOS Computational Biology*, 13(10), e1005831. [https://doi.org/10.1371/journal.pcbi.1005831](https://doi.org/10.1371/journal.pcbi.1005831)


---

## Repository Structure

### **0-data**
This directory contains the analysis outputs extracted from `.xtc` files. Each subdirectory represents a specific analysis and includes:

- **`extract.sh`**: A script to extract data from `.xtc` files.
- **Extracted Data**: Relevant information from `.xtc` files, such as:
  - The coordinate being biased (e.g., z-coordinate for membranes, angles, etc.).
  - Data required for unbiasing using WHAM.

Additionally, the parameters and form of the bias are stored in the `bias_parameters` directory within `0-data`.

---

### **1-wham**
This directory contains scripts and notebooks for constructing bias matrices, calculating weights, and handling the WHAM procedure.

#### **`calc_U_matrix.ipynb`**
- Constructs the bias matrix required for WHAM analysis.
- Details:
  - Number of windows: `N_windows`, indexed as `i = range(0, N_windows)`.
  - Number of samples per window: `N_i`.
  - Total number of samples: `N_samples`.
  - The bias matrix shape: `N_samples x N_windows`. Each element contains the bias a sample would have felt in each window, regardless of its origin.
- If multiple types of biases are acting on the system, all biases should be added here.

#### **`calc_weights.ipynb`**
- Uses a generalized/binless WHAM implementation (more flexible than GROMACS' version).
- Takes the calculated bias matrix as input and outputs:
  - **Weights**: Represent the contribution of each sample to unbiased averages and free energies.
  - **Bootstrapped Weights**: Optional calculation for estimating statistical errors in subsequent analyses.

---

### **3-analysis**
This directory is used for post-WHAM analyses. Using the weights calculated in `1-wham`, you can:

- **Estimate Averages**: Calculate unbiased averages for various observables.
- **Plot Distributions**: Generate reweighted distributions that represent the unbiased ensemble.
- **Joint Distributions**: Combine data from `0-data` with weights to create joint distributions.
- **Statistical Errors**: Estimate statistical errors for all plots and quantities using bootstrapped weights.

---

## Workflow

1. **Extract Data**:
   - Use the scripts in `0-data` to extract biased coordinates and relevant parameters from `.xtc` files.

2. **Construct Bias Matrix**:
   - Run `calc_U_matrix.ipynb` to construct the bias matrix.

3. **Calculate Weights**:
   - Use `calc_weights.ipynb` to compute weights using the WHAM code.
   - Optionally, calculate bootstrapped weights for error estimation.

4. **Analyze Data**:
   - Use the scripts in `3-analysis` to calculate unbiased averages, generate distributions, and estimate statistical errors.

---

## Dependencies
Ensure the following dependencies are installed before running the analysis:

- Python (>=3.7)
- NumPy
- Matplotlib
- Jupyter Notebook
- WHAM code (generalized/binless version)

---


## License
This project is licensed under the [MIT License](LICENSE).


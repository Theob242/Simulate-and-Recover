import numpy as np

def simulate_parameters():
    """ Randomly generate model parameters within the specified range. """
    alpha = np.random.uniform(0.5, 2.0)  # Boundary separation
    nu = np.random.uniform(0.5, 2.0)     # Drift rate
    tau = np.random.uniform(0.1, 0.5)    # Nondecision time
    return alpha, nu, tau

def compute_predicted_statistics(alpha, nu, tau):
    """ Compute predicted accuracy, mean RT, and variance RT using EZ diffusion forward equations. """
    y = np.exp(-nu * alpha)

    R_pred = 1 / (1 + y)  # Eq (1)
    M_pred = tau + (alpha / (2 * nu)) * ((1 - y) / (1 + y))  # Eq (2)
    V_pred = (alpha / (2 * nu**3)) * ((1 - 2 * nu * alpha * y - y**2) / (1 + y)**2)  # Eq (3)

    return R_pred, M_pred, V_pred

def simulate_observed_statistics(R_pred, M_pred, V_pred, N):
    """ Generate noisy observed summary statistics using sampling distributions. """
    # Simulate observed accuracy (Eq 7)
    T_obs = np.random.binomial(N, R_pred)  
    R_obs = T_obs / N  

    # Simulate observed mean RT (Eq 8)
    M_obs = np.random.normal(M_pred, np.sqrt(V_pred / N))  

    # Simulate observed variance RT (Eq 9)
    V_obs = np.random.gamma((N - 1) / 2, (2 * V_pred) / (N - 1))  

    return R_obs, M_obs, V_obs

def recover_parameters(R_obs, M_obs, V_obs):
    """ Recover parameters (ν, α, τ) from observed statistics using EZ diffusion inverse equations. """
    if R_obs <= 0 or R_obs >= 1:  # Prevent log(0) errors
        return None, None, None

    L = np.log(R_obs / (1 - R_obs))  # Log odds ratio

    if V_obs <= 0:  # Prevent sqrt of negative numbers
        return None, None, None

    nu_est = np.sign(R_obs - 0.5) * 4 * np.sqrt((L * (R_obs**2 * L - R_obs * L + R_obs - 0.5)) / V_obs)  # Eq (4)

    if nu_est == 0:  # Prevent division by zero in alpha_est
        return None, None, None

    alpha_est = L / nu_est  # Eq (5)
    tau_est = M_obs - (alpha_est / (2 * nu_est)) * ((1 - np.exp(-nu_est * alpha_est)) / (1 + np.exp(-nu_est * alpha_est)))  # Eq (6)

    return nu_est, alpha_est, tau_est


if __name__ == "__main__":
    # Simulate parameters
    alpha, nu, tau = simulate_parameters()
    
    # Compute predicted summary statistics
    R_pred, M_pred, V_pred = compute_predicted_statistics(alpha, nu, tau)

    # Print predicted values
    print(f"Simulated Parameters:\nBoundary separation (α): {alpha}\nDrift rate (ν): {nu}\nNondecision time (τ): {tau}")
    print(f"\nPredicted Summary Statistics:\nAccuracy Rate (R_pred): {R_pred}\nMean RT (M_pred): {M_pred}\nVariance RT (V_pred): {V_pred}")

    # Simulate observed statistics for different sample sizes and recover parameters
    for N in [10, 40, 4000]:
        R_obs, M_obs, V_obs = simulate_observed_statistics(R_pred, M_pred, V_pred, N)
        nu_est, alpha_est, tau_est = recover_parameters(R_obs, M_obs, V_obs)

        # Compute bias and squared error
        if None not in [nu_est, alpha_est, tau_est]:
            bias = (nu - nu_est, alpha - alpha_est, tau - tau_est)
            squared_error = (bias[0]**2, bias[1]**2, bias[2]**2)
        else:
            bias = (None, None, None)
            squared_error = (None, None, None)

        print(f"\nObserved Statistics for N={N}:")
        print(f"Accuracy Rate (R_obs): {R_obs}")
        print(f"Mean RT (M_obs): {M_obs}")
        print(f"Variance RT (V_obs): {V_obs}")

        print(f"\nRecovered Parameters for N={N}:")
        print(f"Drift rate (ν_est): {nu_est}")
        print(f"Boundary separation (α_est): {alpha_est}")
        print(f"Nondecision time (τ_est): {tau_est}")

        print(f"\nEstimation Bias for N={N}: {bias}")
        print(f"Squared Error for N={N}: {squared_error}")

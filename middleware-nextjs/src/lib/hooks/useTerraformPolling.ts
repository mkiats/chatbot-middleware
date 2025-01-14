// hooks/useInfrastructurePolling.ts
import { useState, useEffect, useCallback } from 'react';
import { TerraformStatus } from '../types/models';

interface InfrastructureStatusResponse {
    name: string;
    instanceId: string;
    runtimeStatus: string;
    input: string;
    customStatus: string | null;
    output: {
        success: boolean;
        message: string;
        status: string;
    } | null;
}

export const useInfrastructurePolling = (statusQueryUri: string | null) => {
    const [status, setStatus] = useState<TerraformStatus>(TerraformStatus.PENDING);
    const [isPolling, setIsPolling] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [output, setOutput] = useState<string | null>(null);

    const pollStatus = useCallback(async () => {
        if (!statusQueryUri) return;

        try {
            const response = await fetch(statusQueryUri);
            if (!response.ok) {
                throw new Error('Failed to fetch status');
            }

            const data: InfrastructureStatusResponse = await response.json();
            
            // Map the status from the response to TerraformStatus
            if (data.output?.status) {
                setStatus(data.output.status as TerraformStatus);
                setOutput(data.output.message);
            }

            // Check if we should stop polling
            if (data.output?.status === TerraformStatus.COMPLETE || 
                data.output?.status === TerraformStatus.FAILED) {
                setIsPolling(false);
            }

        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred while polling');
            setIsPolling(false);
        }
    }, [statusQueryUri]);

    useEffect(() => {
        let intervalId: NodeJS.Timeout;

        if (statusQueryUri && isPolling) {
            // Initial poll
            pollStatus();

            // Set up polling interval (every 5 seconds)
            intervalId = setInterval(pollStatus, 2000);
        }

        return () => {
            if (intervalId) {
                clearInterval(intervalId);
            }
        };
    }, [statusQueryUri, isPolling, pollStatus]);

    const startPolling = useCallback(() => {
        setIsPolling(true);
        setError(null);
    }, []);

    const stopPolling = useCallback(() => {
        setIsPolling(false);
    }, []);

    return {
        status,
        isPolling,
        error,
        output,
        startPolling,
        stopPolling
    };
};
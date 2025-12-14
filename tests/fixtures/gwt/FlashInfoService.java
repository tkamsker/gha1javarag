package com.example.client.servlet;

import com.google.gwt.user.client.rpc.RemoteService;
import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;
import com.example.shared.dto.FlashInfoDTO;

import java.util.List;

/**
 * GWT RPC service interface for Flash Info management.
 * Test fixture for GWT RPC analyzer.
 */
@RemoteServiceRelativePath("flashinfo")
public interface FlashInfoService extends RemoteService {

    /**
     * Create a new flash info message.
     *
     * @param dto Flash info data transfer object
     * @return Created flash info with generated ID
     * @throws RemoteException if creation fails
     */
    FlashInfoDTO createFlashInfo(FlashInfoDTO dto) throws RemoteException;

    /**
     * Update an existing flash info message.
     *
     * @param dto Flash info data transfer object with ID
     * @return Updated flash info
     * @throws RemoteException if update fails
     */
    FlashInfoDTO updateFlashInfo(FlashInfoDTO dto) throws RemoteException;

    /**
     * Delete a flash info message by ID.
     *
     * @param id Flash info ID
     * @return true if deleted successfully
     * @throws RemoteException if deletion fails
     */
    boolean deleteFlashInfo(Long id) throws RemoteException;

    /**
     * Get all flash info messages.
     *
     * @return List of all flash info messages
     * @throws RemoteException if retrieval fails
     */
    List<FlashInfoDTO> getAllFlashInfo() throws RemoteException;

    /**
     * Get flash info by ID.
     *
     * @param id Flash info ID
     * @return Flash info or null if not found
     * @throws RemoteException if retrieval fails
     */
    FlashInfoDTO getFlashInfoById(Long id) throws RemoteException;

    /**
     * Get active flash info messages.
     *
     * @param activeOnly Whether to return only active messages
     * @return List of flash info messages
     */
    List<FlashInfoDTO> getFlashInfoFiltered(boolean activeOnly);
}

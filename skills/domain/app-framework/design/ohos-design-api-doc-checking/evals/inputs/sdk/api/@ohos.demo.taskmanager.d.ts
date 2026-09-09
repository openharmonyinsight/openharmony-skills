/**
 * Provides task management capabilities.
 *
 * @namespace demoTaskManager
 * @since 10
 */
declare namespace demoTaskManager {
  /**
   * Task information.
   *
   * @interface TaskInfo
   * @since 10
   */
  interface TaskInfo {
    /**
     * Task name.
     *
     * @type {string}
     * @since 10
     */
    name: string;

    /**
     * Delay time in ms.
     *
     * @type {number}
     * @since 10
     */
    delay: number;

    /**
     * Task priority.
     *
     * @type {number}
     * @since 10
     */
    priority: number;
  }

  /**
   * Creates a background task.
   *
   * @param {TaskInfo} taskInfo - Indicates the task information.
   * @param {AsyncCallback<number>} callback - Indicates the callback.
   * @throws {BusinessError} 401 - Parameter error.
   * @throws {BusinessError} 801 - Capability not supported.
   * @since 10
   */
  function createTask(taskInfo: TaskInfo, callback: AsyncCallback<number>): void;

  /**
   * Queries all tasks.
   *
   * @returns {Promise<Array<TaskInfo>>} Returns the task list.
   * @throws {BusinessError} 401 - Parameter error.
   * @since 10
   */
  function queryTasks(): Promise<Array<TaskInfo>>;
}

export default demoTaskManager;

const logError = (error, context = {}) => {
  const timestamp = new Date().toISOString();
  const errorInfo = {
    timestamp,
    error: {
      message: error.message,
      stack: error.stack,
      name: error.name
    },
    context: {
      ...context,
      userAgent: navigator.userAgent,
      url: window.location.href
    }
  };

  // Log to console
  console.error('Application Error:', errorInfo);

  // Log to server (if you have an error tracking service)
  // api.logError(errorInfo).catch(console.error);
};

export const withErrorLogging = (fn, context = {}) => {
  return async (...args) => {
    try {
      return await fn(...args);
    } catch (error) {
      logError(error, context);
      throw error;
    }
  };
};

export default logError; 
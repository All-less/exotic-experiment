import qwest from 'qwest';

const ajax = {
  get: async function ajax$get(url, params = {}, options = {}) {
    options.responseType = options.responseType || 'text';
    params.timestamp = params.timestamp || Date.now();
    let res;
    try {
      const xhr = await qwest.get(url, params, options);
      res = JSON.parse(xhr.response);
    } catch (err) {
      throw err;
    }
    if (res.code !== 0) {
      throw res.errors;
    }
    return res.data;
  },
  post: async function ajax$post(url, params = {}, options = {}) {
    options.dataType = options.dataType || 'json';
    options.responseType = options.responseType || 'text';
    let res;
    try {
      const xhr = await qwest.post(url, params, options);
      res = JSON.parse(xhr.response);
    } catch (err) {
      throw err;
    }
    if (res.code !== 0) {
      throw res.errors;
    }
    return res.data;
  }
};

export default ajax;

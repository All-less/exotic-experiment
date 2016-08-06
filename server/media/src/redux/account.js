const CHANGE_FORM = 'Exotic/account/changeForm';

const init = {
  formState: 'login'
};

export const changeForm = (formState) => ({
  type: CHANGE_FORM,
  formState
});

export default (state=init, action) => {
  switch (action.type) {
    case CHANGE_FORM:
      return {
        formState: action.formState
      };
    default:
      return state;
  }
};
